import pymssql

connect = pymssql.connect('172.31.100.153', 'test', 'ls#it*123', 'YS_StoneStore')  # 建立连接
if connect:
    print("连接成功!")

cursor = connect.cursor()  # 创建一个游标对象python里的sql语句都要通过cursor来执行
sql = "select User_Name from SYS_USER"  # 查询数据库信息
cursor.execute(sql)  # 执行sql语句
row = cursor.fetchone()  # 读取查询结果
limit = 10
while row and limit > 0:  # 循环读取所有结果
    print("Name=%s" % (row[0]))  # 输出结果
    row = cursor.fetchone()
    limit -= 1

cursor.close()
connect.close()
