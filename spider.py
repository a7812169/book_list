# import requests
# from bs4 import BeautifulSoup
# from db_connect import OpenDB
# for i in list(range(2,9)):
#     url = "https://book.douban.com/tag/青春?start={}&type=T".format(i*20)
#
#     re = requests.get(url).text
#     bb = BeautifulSoup(re, 'lxml').find_all("div", {"class": "info"})
#     for k in bb:
#
#         try:
#             title = (k.h2.a.get('title'))
#             author = k.find('div', {"class": "pub"}).get_text().split('/')[0].replace(" ","")
#             intro =k.p.get_text()
#             with OpenDB() as con:
#                 sql="INSERT INTO `book_list`.`book_imformation` (`book_name`, `author`, `intro`, `type`) VALUES ('{}', '{}', '{}', '9')".\
#                     format(title,author,intro)
#                 con.execute(sql)
#         except:
#             pass
kk=["1","2"]

x=','.join(kk)
print(x)