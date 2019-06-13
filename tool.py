# coding=utf-8
from db_connect import OpenDB


# 	5	48	823	业务因此一切能力更多质量.	53	6		823	最初的爱情 最后的仪式	2019-04-03 16:24:04	[英]伊恩·麦克尤恩	全书由八个短篇组成，分别从八个位于童年、青春期和青年等不同阶段的男性视角出发，以意识和潜意识交接地带的经验为揭示对象，有时荒唐，有时伤感，有时温柔，有时骇人... 	6	0	22.00元	2010-2			48	江刚	GB81RZEB3372752945111
def get_user_comment():
    with OpenDB()as con:
        # sql = from comment,book_imformation B,user_information U where comment.user_id=U.ssid and comment.book_id=B.ssid"
        sql = "select * from comment,book_imformation B,user_information U,book_list where comment.user_id=U.ssid and comment.book_id=B.ssid and book_list.ssid=comment.book_list order by time desc limit 50"
        con.execute(sql)
        res = con.fetchall()
        sql="SELECT comment_id,sum(like_number) FROM book_list.comment_like_record group by comment_id"
        con.execute(sql)
        res2=con.fetchall()
        comment_dict={i[0]:i[1] for i in res2}

        comment_list = [i for i in res]
        return comment_list,comment_dict

def get_comment_by_book_id(book_id):
    with OpenDB()as con:
        sql = "SELECT * FROM book_list.comment where book_id={} LIMIT 0, 1000".format(book_id)
        con.execute(sql)
        res = con.fetchall()
        comment_list = [i for i in res]
        return comment_list


def get_user_id_by_name(user_name):
    with OpenDB()as con:
        sql = "select ssid from user_information where user='{}'".format(user_name)
        print(sql)
        con.execute(sql)
        res = con.fetchone()[0]
        # print(res[0])
        return res


def get_user_book_list_by_user_name(user_name):
    book_list_list = []
    with OpenDB()as con:
        # sql="select B.book_list_name,B.create_time,B.like_number,B.unlike_number,B.type from comment C,book_list B,user_infomation U where C.user_id=(select ssid from user_information where user='{}'),"
        user_id = get_user_id_by_name(user_name)
        sql = """select B.ssid,B.book_list_name,
        B.create_time,B.like_number,B.unlike_number,
        B.type,U.sum_of_booklist from book_list B,user_book_list U 
        where B.ssid 
        in (select book_list_id from user_book_list where user_id={} and type=1)and U.book_list_id=B.ssid and U.type=1
""".format(user_id)
        print(sql)
        con.execute(sql)
        res = con.fetchall()

        for i in res:
            book_dict = dict(book_list_id=i[0],
                             book_list_name=i[1],
                             create_time=i[2],
                             like_number=i[3],
                             unlike_number=i[4],
                             type=i[5], sum_of_book_list=i[6])
            book_list_list.append(book_dict)
        return book_list_list


def get_list(type, user_id=None):
    if type == "new":
        with OpenDB() as con:
            sql = 'select book_list_name,type,ssid,like_number from book_list order by create_time desc limit 0,10 '
            con.execute(sql)
            res = con.fetchall()
            return res
    elif type == "elite":
        with OpenDB() as con:
            sql = 'select book_list_name,type,like_number,ssid from book_list order by like_number desc limit 0,10'
            con.execute(sql)
            res = con.fetchall()
            return res
    elif type == "you_like":
        if user_id == None:
            return None
        else:
            you_like_book_list = get_you_like(user_id)

            # you_like_book_list : [{ssid:"aaa",like_number:"aaa"}]
            return you_like_book_list


def get_you_like(user_id):
    with OpenDB() as con:
        sql = "select distinct c.user_id from comment c where book_id in (select c.book_id from comment c where c.user_id='{}')".format(
            user_id)
        # 找到 同样  喜欢这个用户喜欢书的相识用户
        con.execute(sql)
        res = con.fetchall()
        print(res)
        same_user_list = []
        for i in res:
            same_user_list.append(i[0])

        same_user_list = same_user_list
        del same_user_list[same_user_list.index(int(user_id))]
        sql = "select book_list from comment where book_id in {}".format(str(tuple(same_user_list)))
        # 找到 同样  喜欢这个用户喜欢书的相识用户 喜欢书 的书单
        con.execute(sql)
        res = con.fetchall()
        book_list = [k[0] for k in res]
        sql = "select sum(c.star_num) total_star,c.book_list,b.book_list_name from comment c,book_list b where c.book_list in{}and b.ssid=c.book_list group by book_list order by total_star desc" \
              "".format(str(tuple(book_list)))
        # 根据书单的被喜欢数排序
        con.execute(sql)
        res = con.fetchall()
        book_like_list = [dict(ssid=k[1], like_number=int(k[0]), book_list_name=k[2]) for k in res]

        return book_like_list


def get_book_infomation_by_type(type=None):
    with OpenDB() as con:
        if not type:
            sql = "select * from book_imformation "

        else:
            sql = "select * from book_imformation where type={}".format(int(type))

        con.execute(sql)
        res = con.fetchall()
        book_list = []
        for i in res:
            book_dict = dict(book_id=i[0],
                             book_name=i[1],
                             update_time=i[2],
                             author=i[3],
                             intro=i[4],
                             like_number=i[9],
                             unlike_number=i[10])
            book_list.append(book_dict)
        return book_list

def get_book_list_by_create_user(user_name):
    user_id=get_user_id_by_name(user_name)
    with OpenDB() as con:
        sql="select * from "


def update_book_information_by_book_id(book_id, like_type):
    with OpenDB() as con:
        if like_type == 1:
            sql = "update book_imformation set like_number=like_number+1 where ssid={}".format(book_id)
            print(sql)
        else:
            sql = "update book_imformation set unlike_number=unlike_number+1 where ssid={}".format(book_id)
        con.execute(sql)

        return True


def delete_book_list_by_book_list_id(book_list_id):
    with OpenDB()as con:
        sql = """DELETE FROM `book_list`.`user_book_list` WHERE (`book_list_id` = '{}')""".format(book_list_id)
        con.execute(sql)
        sql = """DELETE FROM `book_list`.`book_list` WHERE (`ssid` = '{}')""".format(book_list_id)
        con.execute(sql)
    return True


def get_book_list_information_by_book_list_name(book_list_name):
    with OpenDB()as con:
        sql = 'select B.ssid,B.book_name,B.like_number,B.author,B.intro,B.unlike_number,C.comment,C.star_num from comment C,book_imformation B  ' \
              'where C.book_id=B.ssid and C.book_list=(select ssid from book_list where book_list_name={})'.format(
            book_list_name)
        con.execute(sql)
        res = con.fetchall()
        book_list_detail = []
        for i in res:
            book_dict = dict(book_id=i[0],
                             book_name=i[1],
                             like_number=i[2],
                             author=i[3],
                             intro=i[4],
                             unlike_number=i[5],
                             comment=i[6],
                             star_num=i[7], )
            book_list_detail.append([book_dict])
    return book_list_detail,


# def get_book_list_information_by_book_list_id(book_list_id):
#     with OpenDB()as con:
#         sql = "select * from book_list where ssid={}".format(book_list_id)
#         con.execute(sql)
#         res = con.fetchall()
#         book_list_information = []
#         for i in res:
#             book_dict = dict(book_list_id=i[0],
#                              book_list_name=i[1],
#                              create_time=i[2],
#                              like_number=i[3],
#                              unlike_number=i[4],
# )
#             book_list_information.append([book_dict])
#     return book_list_information,
def get_book_list_detail_information_by_book_list_id(book_list_id):
    with OpenDB() as con:
        sql="SELECT * FROM book_list.comment,book_imformation,book_list B where book_list={} and book_imformation.ssid=comment.book_id and B.ssid=book_list".format(book_list_id)
        con.execute(sql)
        res=con.fetchall()
        book_list = []
        for i in res:
            book_dict = dict(
                book_id=i[2],
                book_name=i[8],
                comment=i[3],
                star_num=i[5],
                author=i[10],
                intro=i[11],
                book_list_intro=i[-1],
                like_number=i[-9],
                unlike_number=i[-8],
                book_list_name=i[-6])
            book_list.append(book_dict)
        print(book_list)
        return book_list
def get_all_book_list_infomation():
    with OpenDB() as con:
        sql = "select*,count(book_list_name)from book_list l,user_book_list UB,user_information U,comment C where C.user_id=U.ssid and C.book_list=l.ssid and l.ssid=UB.book_list_id and U.ssid=UB.user_id group by book_list_name"
        con.execute(sql)
        res = con.fetchall()
        book_list = []
        for i in res:
            book_dict = dict(
                book_list_id=i[0],
                book_list_name=i[1],
                create_time=i[2],
                like_number=i[3],
                type=i[5],
                unlike_number=i[4],
                created_userid=i[13],
                sum_of_booklist=i[-1])
            book_list.append(book_dict)

        return book_list


def get_user_focus_list(user_name):
    with OpenDB() as con:
        user_id = get_user_id_by_name(user_name)
        sql = "select book_list_id from user_book_list where user_id={} and type=2 ".format(user_id)
        con.execute(sql)
        res = con.fetchall()
        user_focus_list = []
        for i in res:
            user_focus_list.append(i[0])
        return list(set(user_focus_list))


def page():
    total_information = get_all_book_list_infomation()
    total_page = int(len(total_information) / 10)
    return total_page


def update_like_number_by_user_id(user_id, book_list_id):
    with OpenDB() as con:
        sql = """UPDATE `book_list`.`book_list` SET like_number=like_number+1 WHERE (`ssid` = '{}');
""".format(book_list_id)
        con.execute(sql)
        sql = """INSERT INTO `book_list`.`user_like_book_record` (`user_id`, `book_list_id`, `like_number`) VALUES ('{}', '{}', '1');

""".format(user_id, book_list_id)

        con.execute(sql)


def get_user_information(user_id=None):
    if not user_id:
        with OpenDB() as con:
            sql = """	SELECT * FROM book_list.user_information"""
            con.execute(sql)
            res = con.fetchall()
            return res


def insert_new_user(user_name, password):
    with OpenDB() as con:
        sql = """INSERT INTO `book_list`.`user_information` (`user`, `password`) VALUES ('{}', '{}')
""".format(user_name, password)
        con.execute(sql)
        return True


def delete_user_information_by_user_id(user_id):
    with OpenDB() as con:
        sql = """DELETE FROM `book_list`.`user_information` WHERE (`ssid` = '{}')
""".format(user_id)
        con.execute(sql)
        return True


def update_user_password_by_user_id(user_id, passowrd):
    with OpenDB() as con:
        sql = """UPDATE `book_list`.`user_information` SET `password` = '{}' WHERE (`ssid` = '{}')""".format(passowrd,
                                                                                                             user_id)
        con.execute(sql)
        return True
def search_book_name(book_name):
    with OpenDB() as con:
        print(book_name)
        if book_name=="":
            return None
        sql="select book_name,author from book_imformation where book_name like '%{}%'".format(book_name)
        con.execute(sql)
        res=con.fetchall()
        k=[]
        for i in res:
            book_name=i[0]
            author=i[1]
            k.append({"book_name":book_name,"author":author})
        return k
def get_book_information_by_book_name(book_name):
    with OpenDB() as con:

        sql = "select * from book_imformation where book_name='{}'".format(book_name)
        print(sql)
        con.execute(sql)
        res = con.fetchone()
        print(res)
        book_list = []

        book_dict = dict(book_id=res[0],
                         book_name=res[1],
                         update_time=res[2],
                         author=res[3],
                         intro=res[4],
                         like_number=res[9],
                         unlike_number=res[10])
        book_list.append(book_dict)
        print(book_list)
        return book_list
def insert_new_book_list(book_title_name,user_name,book_intro,book,comment):
    with OpenDB() as con:
        sql="select * from book_list where book_list_name='{}'".format(book_title_name)
        con.execute(sql)
        if len(con.fetchall())<1:
            sql="INSERT INTO `book_list`.`book_list` (`book_list_name`,`book_list_intro`) VALUES ('{}','{}')".format(book_title_name,book_intro)
            con.execute(sql)
        sql="select ssid from book_list where book_list_name ='{}'".format(book_title_name)
        con.execute(sql)
        user_id=get_user_id_by_name(user_name)
        book_list_id=con.fetchone()[0]
        book_id=get_book_information_by_book_name(book)[0]['book_id']
        sql="INSERT INTO `book_list`.`comment` (`user_id`, `book_id`, `comment`, `book_list`, `star_num`) VALUES ('{}', '{}', '{}', '{}', '{}')"\
            .format(user_id,book_id,comment,book_list_id,5)
        con.execute(sql)
        sql="select * from user_book_list where user_id ='{}'and book_list_id='{}'".format(user_id,book_list_id)
        con.execute(sql)
        if len(con.fetchall())<1:
            sql="INSERT INTO `book_list`.`user_book_list` (`user_id`, `book_list_id`, `type`) VALUES ('{}', '{}', '{}')".format(user_id,book_list_id,1)
            print(sql)
            con.execute(sql)
        return True
def get_user_other_book_list_by_user_name(user_nane):
    user_id=get_user_id_by_name(user_nane)
    with OpenDB() as con:
        sql="SELECT * FROM book_list.user_book_list,book_list where user_id={} and book_list_id=book_list.ssid group by book_list_id".format(user_id)
        con.execute(sql)
        ress=con.fetchall()
        book_list=[]
        for res in ress:
            book_dict = dict(user_id=res[1],
                             book_list_id=res[2],
                             book_list_name=res[6])
            book_list.append(book_dict)
        return book_list