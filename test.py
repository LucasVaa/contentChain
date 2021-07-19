#导入依赖包
#!/usr/bin/python3
 
import psycopg2
 
#创建连接对象
conn=psycopg2.connect(database="postgres",user="postgres",password="123456",host="localhost",port="5432")
cur=conn.cursor() #创建指针对象
 
# 创建表
cur.execute("CREATE TABLE student(id integer,name varchar,sex varchar);")
 
#插入数据
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(1,'Aspirin','M'))
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(2,'Taxol','F'))
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(3,'Dixheral','M'))
 
# 获取结果
cur.execute('SELECT * FROM student')
results=cur.fetchall()
print (results)
 
# 关闭练级
conn.commit()
cur.close()
conn.close()