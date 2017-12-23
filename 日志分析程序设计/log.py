#!/usr/bin/env python
# -*- coding: utf-8-*-
import json, redis, hashlib, time,pymssql
#读取Redis数据
r = redis.Redis(host='172.19.1.251', port=6379, db=0)
w = redis.Redis(host='172.19.1.251', port=6379, db=1)
Key = 'filebeat'
data = r.lrange(Key, -10, r.llen('Key')-1)
w.flushdb()
#设置SQL链接函数
class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        #查询完毕后必须关闭连接
        self.conn.close()
        return resList
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
#生成MD5值函数
def get_hash(name):
    md5 = hashlib.md5()
    md5.update(str.encode(name))
    return md5.hexdigest()
#生成MD5值并存储进入Redis
def Set_Url(IP,Server,Code):
    ip_md5 = get_hash(IP)
    if w.hexists('IP_Hash', ip_md5):
        w.zincrby('IP', ip_md5, amount=1)
    else:
        w.hset('IP_Hash', ip_md5, IP)
        w.zadd('IP', ip_md5, 1)
    server_md5 = get_hash(Server)
    if w.hexists('Server_Hash', server_md5):
        w.zincrby('Server', server_md5, amount=1)
    else:
        w.hset('Server_Hash', server_md5, Server)
        w.zadd('Server', server_md5, 1)
    code_md5 = get_hash(Code)
    if w.hexists('Code_Hash', code_md5):
        w.zincrby('Code', code_md5, amount=1)
    else:
        w.hset('Code_Hash', code_md5, Code)
        w.zadd('Code', code_md5,1)
# 获取数据并写入Redis
Time_interval = 60
LocalTime = int(time.time())
Flow_Input_Sum = 0
Flow_Output_Sum = 0
Conn_List = []
a = 0
for i in data:
    log = (i.decode())
    json_log = json.loads(log)
    HostName = json_log['beat']['name']
    Message = json_log['message']
    try:
        Log = json.loads(Message)
    except:
        pass
    Old_Date = Log['local_date_time'].split()
    Date = Old_Date[0]
    ID_time = int(time.mktime(time.strptime(Date, '%d/%b/%Y:%H:%M:%S')))
    Date_diff = LocalTime - ID_time
    if Date_diff < Time_interval:
        IP = Log['client_ip']
        Server = Log['server_name']
        Code = Log['status_code']
        Input = int(Log['bytes_uploaded'])
        Output = int(Log['bytes_read'])
        Conn = int(Log['actconn'])
        Flow_Input = (Input) / 1048576
        Flow_Output =(Output) / 1048576
        Flow_Input_Sum = Flow_Input_Sum +Flow_Input
        Flow_Output_Sum = Flow_Output_Sum +Flow_Output
        Conn_List.append(Conn)
        Set_Url(IP, Server, Code)
        a += 1
#进行数据统计
def get_data(Data,Hash,Name):
    for ID in Data:
        ID_hash = ID[0].decode()
        ID_Num = int(ID[1])
        ID_code = w.hget('%s' % Hash, ID_hash).decode()
        Code_Sql = '''
        INSERT INTO dbo.%s
                ( Date, %s, Number )
        VALUES  ( '%s', -- Date - date
                  '%s', -- Code - nchar(10)
                  '%s'  -- Number - nchar(10)
                  )
        ''' % (Name,Name,DATE, ID_code, ID_Num)
        try:
            ms.ExecNonQuery(Code_Sql.encode('utf-8'))
        except:
            print(Code_Sql)
def GetDate():
    IP_list = w.zrevrange('IP', 0, 9, 'whothscores')
    Code_list = w.zrevrange('Code', 0, -1, 'whothscores')
    Server_list = w.zrevrange('Server', 0, -1, 'whothscores')
    get_data(IP_list,'IP_Hash','IP')
    get_data(Code_list,'Code_Hash','Code')
    get_data(Server_list,'Server_Hash','Server')
#输出统计数据
DATE = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
Flow_Sum = Flow_Input_Sum +Flow_Output_Sum
IP_Sum = w.hlen('IP_Hash')

#建立SQL链接
ms = MSSQL(host="xx",user="xx",pwd="xx",db="Conn")
GetDate()
#插入汇总信息SQL
Sum_Sql = '''INSERT INTO dbo.Sum( Name ,Date ,Flow ,Flow_Input_Sum ,Flow_Output_Sum ,Connect ,UV)
            VALUES  ( N'Haproxy' ,'%s',%.2f,%.2f,%.2f,%d,%d)'''% (DATE,Flow_Sum,Flow_Input_Sum,Flow_Output_Sum,int(max(Conn_List)),IP_Sum)
#执行插入操作
try:
    ms.ExecNonQuery(Sum_Sql.encode('utf-8'))
except:
    print(Sum_Sql)
