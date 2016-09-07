# LightMyPy
A lightweight python class to manipulate MySQL database.

### How to use

```python

# config info, necessary parameters host, port, user, passwd, db
dbconfig = {'host':'127.0.0.1',
'port': 3306,
'user':'danfengcao',
'passwd':'123456',
'db':'test',
'charset':'utf8'}

db = LightMysql(dbconfig)

# use select() to select or show
sql_select = "SELECT * FROM Customer"
result_all = db.select(sql_select) # return all data
result_count = db.select(sql_select, 'count') # return number of lines
result_one = db.select(sql_select, 'one') # return one row

# use dml() to insert, update and delete
sql_update = "update Customer set Cost=2 where Id=2"
db.dml(sql_update)
sql_insert = "insert into Customer value(1,'abc')"
result_insert = db.dml(sql_insert)

# user query() to other operations
sql_query = "create table test0 (`ShowMapID` int(11))"
result_query = db.query(sql_query)

```
