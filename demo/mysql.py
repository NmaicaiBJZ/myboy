from pymysql import *

conn = connect(host='localhost',port=3306,user='root',password='123456',database='students',charset='utf8')
               #数据库IP，端口，数据库名，数据库密码，选择的数据库，编码
cs = conn.cursor()

count = cs.execute('select * from students;')

stock_infos = cs.fetchall()
cs.close()
conn.close()

print(str(stock_infos))