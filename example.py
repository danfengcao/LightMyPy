#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LightMysql import LightMysql

if __name__ == '__main__':

    # 配置信息，其中host, port, user, passwd, db为必需
    dbconfig = {'host':'127.0.0.1',
                'port': 3306,
                'user':'danfengcao',
                'passwd':'123456',
                'db':'test',
                'charset':'utf8'}

    db = LightMysql(dbconfig) # 创建LightMysql对象，若连接超时，会自动重连

    # 查找(select, show)都使用select()函数
    sql_select = "SELECT * FROM Customer"
    result_all = db.select(sql_select) # 返回全部数据
    result_count = db.select(sql_select, 'count') # 返回有多少行
    result_one = db.select(sql_select, 'one') # 返回一行

    # 增删改都使用dml()函数
    sql_update = "update Customer set Cost=2 where Id=2"
    result_update = db.dml(sql_update)
    sql_delete = "delete from Customer where Id=2"
    result_delete = db.dml(sql_delete)
    sql_insert = "insert into Customer value(1,'abc')"
    result_delete = db.dml(sql_insert)
    #其它操作
    sql_query = "replace into Customer value(1,'abc')"
    result_query = db.query(sql_query)

    print result_all
    print result_count
    print result_one
