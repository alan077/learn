#!/usr/bin/env python
# -*- coding: utf-8-*-
import time, pymssql


# 设置SQL链接函数
class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


Time = time.time() - 604800
# Old_DATE = time.strftime('%Y-%m-%d',time.localtime(Time))
Old_DATE = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Time))
DATE = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 查询会员数
Member_Conn = MSSQL(host="172.19.3.13", user="Zerostadmin", pwd="$1Urd@$isJ@123.com", db="MembershipCloud")
Member_Sql = 'SELECT COUNT(MemberSN) FROM dbo.MemberBasic;'
Member_List = Member_Conn.ExecQuery(Member_Sql.encode('utf-8'))
Member = Member_List[0][0]
# 查询商家数
Store_Conn = MSSQL(host="172.19.3.13", user="Jewelryadmin", pwd="6Im$E05oLV@123.com", db="MerchantCloud")
Store_Sql01 = "SELECT COUNT(StoreId) FROM dbo.StoreBasic"
Store_Sql04 = "SELECT COUNT(*)  FROM dbo.StorePack WHERE MarketingCloudPackageType = 3"
Store_Sql05 = "SELECT COUNT(*)  FROM dbo.StorePack WHERE MarketingCloudPackageType = 7"
Store_List = Store_Conn.ExecQuery(Store_Sql01.encode('utf-8'))
Store = Store_List[0][0]
TryStore = Store_Conn.ExecQuery(Store_Sql04.encode('utf-8'))[0][0]
PackStore = Store_Conn.ExecQuery(Store_Sql05.encode('utf-8'))[0][0]
# 查询消费数量
Store_Expense = MSSQL(host="172.19.3.13", user="Zerostadmin", pwd="$1Urd@$isJ@123.com", db="MarketingCloud")
Store_Sql02 = "SELECT COUNT(StoreSN) FROM LogBalanceStore WHERE CreateTime >= '%s'  GROUP BY StoreSN" % Old_DATE
Store_Sql03 = "SELECT SUM(CASE WHEN ChangeType = 2101 THEN UsedPrice ELSE 0 END) AS '消费单' FROM dbo.LogBalanceStore WHERE CreateTime >='%s'" % Old_DATE
Expense_list = Store_Expense.ExecQuery(Store_Sql03.encode('utf-8'))
Expense = Expense_list[0][0]
ActiveStore = len(Store_Expense.ExecQuery(Store_Sql02.encode('utf-8')))
InActiveStore = Store - ActiveStore
# 查询ERP数据
ERP_Conn = MSSQL(host="172.19.3.13", user="Jewelryadmin", pwd="6Im$E05oLV@123.com", db="StockingCloud")
ERPStoreSQL = 'SELECT COUNT(StoreId) FROM StockingCloud.dbo.GoodsBasic GROUP BY StoreId  HAVING COUNT(StoreId) >1000  ORDER BY COUNT(StoreId) '
GoodsBasicSQL = 'SELECT COUNT(*) FROM StockingCloud.dbo.GoodsStone'
ERPStore = len(ERP_Conn.ExecQuery(ERPStoreSQL.encode('utf-8')))
GoodsBasic = ERP_Conn.ExecQuery(GoodsBasicSQL.encode('utf-8'))[0][0]
# print(ERPStore)
# print(GoodsBasic)
# 插入数据库
ms = MSSQL(host="172.19.2.200", user="sa", pwd="lcb@123.com", db="Conn")
Old_Store_Sql = "SELECT TOP 1 * FROM dbo.Member  ORDER BY Date DESC"
Old_Store_List = ms.ExecQuery(Old_Store_Sql.encode('utf-8'))
Old_Store = Old_Store_List[0][3]
IncreasedStore = Store - Old_Store
Data = "INSERT INTO dbo.Member( Date ,Member ,Store ,IncreasedStore,TryStore,PackStore,Expense,ActiveStore ,InActiveStore,ERPStore,GoodsBasic) VALUES  ( '%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % (
DATE, Member, Store, TryStore, PackStore, IncreasedStore, Expense, ActiveStore, InActiveStore, ERPStore, GoodsBasic)
print(Data)
# ms.ExecNonQuery(Data.encode('utf-8'))
