from pymysql import connect
class OpenDB(object):
    def __init__(self):
        # 初始化
        self.conn = connect("120.79.227.7", "root", "7812169", "book_list",charset='utf8')
        self.cs = self.conn.cursor()

    def __enter__(self):
        # 返回游标进行执行操作
        return self.cs

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 结束提交数据并关闭数据库
        self.conn.commit()
        self.cs.close()
        self.conn.close()

###########################使用前导入以上模块#################################
