# LightMyPy
Lightweight python class to manipulate MySQL database.

### How to use

```python

# 配置信息，其中host, port, user, passwd, db为必需
dbconfig = {'host':'127.0.0.1',
'port': 3306,
'user':'danfengcao',
'passwd':'123456',
'db':'test',
'charset':'utf8'}

db = LightMysql(dbconfig) # 创建LightMysql对象，若连接超时，会自动重连

# 查找(select, show)都使用select()
sql_select = "SELECT * FROM Customer"
result_all = db.select(sql_select) # 返回全部数据
result_count = db.select(sql_select, 'count') # 返回有多少行
result_one = db.select(sql_select, 'one') # 返回一行

# 增删改都使用dml()
sql_update = "update Customer set Cost=2 where Id=2"
db.dml(sql_update)
sql_insert = "insert into Customer value(1,'abc')"
result_insert = db.dml(sql_insert)
#其它操作
sql_query = "create table test0 (`ShowMapID` int(11))"
result_query = db.query(sql_query)

```
