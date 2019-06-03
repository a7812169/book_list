import  requests
from bs4 import BeautifulSoup
import pymysql

# 打开数据库连接

# SQL 插入语句

def run(n):
    db = pymysql.connect("120.79.227.7", "root", "7812169", "book_list")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    kkk=requests.get('https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T'.format(n))
    kkk.encoding=kkk.apparent_encoding
    soup=BeautifulSoup(kkk.text,'lxml')
    s=soup.find_all('li',{"class":"subject-item"})
    for k in s:
        title=k.find('h2').a.get('title')
        sumary_list=k.find('div',{"class":"pub"}).get_text().replace(' ','').replace('\n','').split('/')
        author=sumary_list[0]
        money=sumary_list[-1]
        time=sumary_list[-2]
        intro=k.find('div',{"class":"info"}).p
        if intro:
            intro=intro.get_text()
        sql = """INSERT INTO `book_list`.`book_imformation`(`book_name`, `author`, `intro`, `money`, `publish_time`) VALUES ('{}', '{}', '{}', '{}', '{}')""".format(title,author,intro,money,time)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

            print('成功',title)
        except:
            # 如果发生错误则回滚
            db.rollback()
            continue
        # 关闭数据库连接
        # db.close()
    db.close()
for i in range(8,100):
    number=i*20
    print(number)
    run(number)