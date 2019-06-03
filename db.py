import pymysql
import random
from faker import Faker  # 打开数据库连接

db = pymysql.connect("120.79.227.7", "root", "7812169", "book_list")
for i in range(1, 104):
    user_id = i
    book_list_id =i
    sql = "INSERT INTO `book_list`.`user_book_list` (`user_id`, `book_list_id`, `type`) VALUES ('{}', '{}', '{}')".format(user_id,book_list_id,2)
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
# 使用cursor()方法获取操作游标
# number = random.randint(0, 1000)
# # if i==100:
# #     break
# # print(i)
# cursor = db.cursor()
# # fake = Faker("zh_CN")
# # # SQL 插入语句
# # user_id=random.randint(0,100)
# # book_id=random.randint(5,1000)
# # book_list=random.randint(0,104)
# # comment=fake.sentence()
# # star_num=random.randint(0,11)
# sql = "UPDATE `book_list`.`book_imformation` SET `type` = {} WHERE `ssid` ={}".format(random.randint(0,13),i)
# # 执行sql语句
# print(sql)
# cursor.execute(sql)
# 提交到数据库执行

# sql='select '
