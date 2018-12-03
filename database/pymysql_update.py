"""
    sql params is tuple
"""
import pymysql

host = "localhost"
user = "root"
password = "root"
database = "world"
charset = "utf8"

db = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)

cursor = db.cursor()

try:
    insert_sql = "insert into user(id,name) values (%s,%s)"
    
    cursor.execute(insert_sql, (4, 'jerry'))
    db.commit()
except:
    print("update fail ")
finally:
    cursor.close()
    db.close()
