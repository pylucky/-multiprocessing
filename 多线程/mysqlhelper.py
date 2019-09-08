
import pymysql
# 创建mysql相关的类
class MysqlHelper(object):
    # 初始化函数, 实例化的时候自动执行
    def __init__(self):
        # 连接mysql的代码
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',database='fangchan', charset='utf8')
        # 创建游标, 目的是为了执行sql语句
        self.cursor = self.db.cursor()

    # 这个函数是我们会反复调用的函数, 目的是执行sql语句, sql是要执行的语句, data是需要插入的数据
    def execute_modify_sql(self, sql,data=None):
        try:
            # 执行
            self.cursor.execute(sql,data)
            # 数据库的提交
            self.db.commit()
            print("----插入成功------")
        except Exception as e:
            print(e,"---------插入失败-----------")

    ##查询
    def query_sql(self,sql):
        try:
            # 执行
            content=[]
            self.cursor.execute(sql)
            data=self.cursor.fetchall()
            for i in data:
                content.append(i)
            return content
        except Exception as e:
            print("出错了,请检查SQL语句----------")
            self.db.callback()
    ##修改
    def update_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("出错了,请检查SQL语句----------")
            self.db.rollback()
    ##删除
    def delete_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("删除成功啦")
        except Exception as e:
            print("出错了,请检查SQL语句----------")
            self.db.rollback()

    # 析构函数, 本个对象再也没有人使用以后, 这个函数自动执行
    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.db.close()

if __name__ == '__main__':
    mysql = MysqlHelper()
    from new_file import md5value

    ##增加

    #
    # print(mysql.execute_modify_sql(sql,data))
    # #查询
    # sql="select * from office_rent order by crawl_time desc limit 10 "
    # mysql=MysqlHelper()
    # print(mysql.query_sql(sql))

    ##修改
    # sql = "update office_rent order set province='北京省' where id ='1935' "
    # mysql = MysqlHelper()
    # mysql.update_sql(sql)
    # print('Mysql连接成功')
    # ##删除
    # sql = "delete from office_rent order by id desc limit 1"
    # mysql = MysqlHelper()
    # print(mysql.delete_sql(sql))

    #
    # ##关于 数据重复 MD5存在 updtae,不存在insert
    # md5 = md5value('诚盈中心'+'18'+'6')
    # count_sql = "select count(id) from office_rent where MD5 = '{MD5}'".format(MD5=md5)
    # print(count_sql)
    # data=mysql.query_sql(sql=count_sql)
    # print(data)
    #
    # ##返回 1 已存在
    # if data[0][0]>0:
    #     ##更新
    #     sql="update office_rent set status=1 where name='诚盈中心' and rent_month='18' and rent_day='6' "
    #     mysql.update_sql(sql)
    #     print("数据重复，更新状态为1")
    # else:
    #     ##添加
    #     sql = 'insert into office_rent(name,rent_month,rent_day,area,crawl_time,site,url,city,MD5,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #
    #     data=('诚盈中心', '18', '6', '1000', '2019-07-28 11:13:46', 'houyi_58tc', 'https://bj.58.com/zhaozu/38924631148436x.shtml', '北京',md5, '0')
    #     print("数据不重复，允许插入")
    #     mysql.execute_modify_sql(sql,data)
