import pymysql
class Mysql_Object():
    def __init__(self,host,user,password,database,port=3306,charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port=port
        self.charset = charset

    def select_sql(self,sql,size=0):
        self.con = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='12root',
            db='cli_db',
            charset='utf8'
        )
        self.cur = self.con.cursor() # 建立游标
        self.sql = sql
        # 判断是否是查询语句
        if self.sql.startswith('select'):
            self.cur.execute(self.sql) # 执行sql语句
            self.count = self.cur.rowcount # 统计查询记录条数
            if size == 0:
                self.res=self.cur.fetchall() # 获取所有查询结果
            elif self != 0:
                self.res=self.cur.fetchmany(size)
            self.cur.close()
            self.con.close()
        return  self.count,self.res

    # 增删改功能
    def excute_sql(self,sql):
        self.con = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='12root',
            db='cli_db',
            charset='utf8'
        )
        self.cur = self.con.cursor()  # 建立游标
        self.sql = sql
        if self.sql.startswith('insert'):
            self.cur.execute(self.sql) #执行语句
            self.con.commit()
            self.cur.close()
            self.con.close()
        elif self.sql.startswith('delete'):
            self.cur.execute(self.sql)  # 执行语句
            self.con.commit()
            self.cur.close()
            self.con.close()
        elif self.sql.startswith('update'):
            self.cur.execute(self.sql)  # 执行语句
            self.con.commit()
            self.cur.close()
            self.con.close()