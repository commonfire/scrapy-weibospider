from  datamysql import MysqlStore
d = MysqlStore()
conn = d.get_connection()
sql = "select * from t_user_follow"
cursor = d.select_operation(conn,sql)

for i in range(100):
    print 'i:',i
    for result in cursor.fetchmany(5):
        if result[1]:
            print 'hhhhhhh'
