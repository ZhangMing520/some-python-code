"""
    pip install PyMySQL
    
    fetch 返回内容是元组
"""

import pymysql

host = "localhost"
user = "root"
password = "root"
database = "sakila"
charset = "utf8"

db = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)

sql = "select t.* from city t "
cursor = db.cursor()

try:
    cursor.execute(sql)
    print(cursor.rowcount)
    
    # result = cursor.fetchone()
    # while result is not None:
    #     print(result)
    #     result = cursor.fetchone()
    
    results = cursor.fetchall()
    # cursor.fetchmany(size)
    for result in results:
        print(result)

except:
    print("unable to fetch data ")
finally:
    cursor.close()
    db.close()
