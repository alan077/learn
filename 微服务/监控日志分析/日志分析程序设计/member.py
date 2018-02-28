#!/usr/bin/env python
# -*- coding: utf-8-*-
import time,pymssql
#����SQL���Ӻ���
class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"û���������ݿ���Ϣ")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"�������ݿ�ʧ��")
        else:
            return cur
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        #��ѯ��Ϻ����ر�����
        self.conn.close()
        return resList
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
Time = time.time() -604800
Old_DATE = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(Time))
DATE = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#��ѯ��Ա��
Member_Conn = MSSQL(host="xx",user="xx",pwd="xx",db="Conn")
Member_Sql = 'SELECT COUNT(MemberSN) FROM dbo.MemberBasic;'
Member_List = Member_Conn.ExecQuery(Member_Sql.encode('utf-8'))
Member = Member_List[0][0]
#��ѯ�̼���
Store_Conn = MSSQL(host="xx",user="xx",pwd="xx",db="Conn")
Store_Sql01 = "SELECT COUNT(StoreSN) FROM dbo.StoreBasic"
Store_Sql02 = "SELECT COUNT(StoreSN) FROM LogBalanceStore WHERE CreateTime >= '%s'  GROUP BY StoreSN" % Old_DATE
Store_List = Store_Conn.ExecQuery(Store_Sql01.encode('utf-8'))
Store = Store_List[0][0]
ActiveStore = len( Store_Conn.ExecQuery(Store_Sql02.encode('utf-8')))
InActiveStore = Store - ActiveStore
print(Old_DATE,DATE,Member,Store,ActiveStore,InActiveStore)
#�������ݿ�
ms = MSSQL(host="xx",user="xx",pwd="xx",db="Conn")
Data = "INSERT INTO dbo.Member( Date ,Member ,Store ,ActiveStore ,InActiveStore) VALUES  ( '%s',%d,%d,%d,%d)" %(DATE,Member,Store,ActiveStore,InActiveStore)
ms.ExecNonQuery(Data.encode('utf-8'))