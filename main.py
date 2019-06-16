# -*- coding: UTF-8 -*-
from flask import Flask
import json
from flask import request, flash, url_for, redirect,jsonify
from flask import render_template, session
import tool
from db_connect import OpenDB
from flask import flash, get_flashed_messages

app = Flask(__name__)
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'


# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        with OpenDB()as con:
            sql = 'select user,password from user_information where user="{}"and password="{}"'.format(user, password)
            # try:
            con.execute(sql)
            number = len(con.fetchall())
            if number == 0:
                flash('')
                print('账号或密码错误，请重新aaa登陆')

                return render_template('登录框.html')
            else:
                print('登录成功')
                session['user_name'] = user
                return redirect(url_for('index'))
    else:
        return render_template('登录框.html')


# 注册
@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            pass
        else:
            flash('密码不一致')
        with OpenDB() as con:
            sql = 'select user from user_information where user="{}"'.format(user)
            con.execute(sql)
            if len(con.fetchall()) > 0:
                return redirect(url_for('regist'))
            else:
                sql = 'insert into user_information(`user`,`password`)values("{}","{}")'.format(user, password)
                try:
                    con.execute(sql)
                    session['user_name'] = user
                    return redirect(url_for('index'))
                except:
                    print('发生位置错误，无法插入')
        return render_template('zhuceye.html')
    else:
        return render_template('zhuceye.html')


# 入口首页
@app.route('/index', methods=['POST', 'GET'])
def index():
    comment_id=request.form.get('comment_id')
    like_book_ssid = request.args.get('ssid')
    user_name = session.get('user_name')
    if user_name:
        user_id=tool.get_user_id_by_name(user_name)
    else:
        user_id=None
    if comment_id:
        with OpenDB() as con:
            user_id = tool.get_user_id_by_name(user_name)
            sql="INSERT INTO `book_list`.`comment_like_record` (`comment_id`, `user_id`) VALUES ('{}', '{}')".format(comment_id,user_id)
            con.execute(sql)
    if request.args.get('type'):
        book_list_id = request.args.get('book_list_id')
        user_id = tool.get_user_id_by_name(user_name)
        tool.update_like_number_by_user_id(user_id, book_list_id)
    if like_book_ssid:
        with OpenDB() as con:
            sql = 'select user from user_information where user="{}"'.format(user_name)
            con.execute(sql)
    # todo 这里以后需要写个sql 转换ssid
    new_list = tool.get_list("new", user_id=None)
    # 最新漂流
    elite_list = tool.get_list("elite", user_id=None)
    # 精品书单
    your_like_list = tool.get_list("you_like", user_id=user_id)
    comment_list,comment_dict = tool.get_user_comment()
    # comment_list_by_book=tool.get_comment_by_book_id()
    return render_template('index.html', new_list=new_list, elite_list=elite_list, your_like_list=your_like_list,
                           comment_list=comment_list[:30],comment_dict=comment_dict,
                           user_name=user_name)


@app.route('/all_book_list', methods=['POST', 'GET'])
def all_book_list():
    user_name = session.get('user_name')
    book_list = tool.get_all_book_list_infomation()
    total_page = tool.page()
    now_page = request.args.get('page')
    if user_name:
        user_focus_list = tool.get_user_focus_list(user_name)
    else:
        user_focus_list = None
    if not now_page:
        now_page = 1

    data = 10 * int(now_page)
    data2 = 10 * (int(now_page) + 1)
    if not len(book_list)<10:
        book_list = book_list[data:data2]
    return render_template('all_book_list.html', book_list=book_list, user_focus_list=user_focus_list,
                           total_page=list(range(total_page)), now_page=int(now_page))


@app.route('/my_focus_list', methods=['POST', 'GET'])
def my_focus_list():
    user_name = session.get('user_name')
    book_list = tool.get_user_book_list_infomation_by_user_name(user_name)
    total_page = tool.page()
    now_page = request.args.get('page')
    if user_name:
        user_focus_list = tool.get_user_focus_list(user_name)
        print(user_focus_list)
    else:
        user_focus_list = None
    if not now_page:
        now_page = 1

    data = 10 * int(now_page)
    data2 = 10 * (int(now_page) + 1)
    if not len(book_list) < 10:
        book_list = book_list[data:data2]
    return render_template('my_focus_list.html', book_list=book_list,
                           total_page=list(range(total_page)), now_page=int(now_page))

# 图书分类
@app.route('/category', methods=['POST', 'GET'])
def category():
    user_name = session.get('user_name')
    book_type = request.args.get('book_type')
    print(book_type)
    from tool import get_book_infomation_by_type
    total_book_list = get_book_infomation_by_type(book_type)
    max_page = list(range(int(len(total_book_list) / 9)))

    print(max_page)
    page = request.args.get('page')
    if not page:
        page = 1
    page=int(page)
    this_page_book_list = total_book_list[int(page) * 9:(int(page) + 1) * 9]
    return render_template('fenlei.html', this_page_book_list=this_page_book_list, book_type=book_type, now_page=page,
                           max_page=max_page,user_name=user_name)


# 选择点击喜好
@app.route('/category/like_or_no_like', methods=['GET'])
def like_or_like():

    book_id = request.args.get('book_id')
    # 记得写1为喜欢0为不喜欢
    like_or_not = request.args.get('like_or_not')
    print(book_id,like_or_not)
    if like_or_not:
        tool.update_book_information_by_book_id(book_id, 1)
    else:
        tool.update_book_information_by_book_id(book_id,None)
    return redirect(url_for('category'))


# 用户书单

@app.route('/user_book_list', methods=['GET', 'POST'])
def user_book_list():
    user_name = session.get('user_name')
    book_list = tool.get_user_book_list_by_user_name(user_name)
    if request.method == 'POST':
        book_list_id = request.form['book_list_id']
        tool.delete_book_list_by_book_list_id(book_list_id)
        return redirect(url_for('user_book_list', book_list=book_list))
    return render_template('my_list.html', book_list=book_list)


# 书单详情界面

@app.route('/book_list', methods=['GET'])
def book_list():
    user_name = request.args.get('user_name')
    book_list_name = request.args.get('book_list_name')


@app.route('/outlogin', methods=['POST', 'GET'])
def outlogin():
    url = request.args.get('back_url')
    session.pop('user_name')
    return redirect(url_for(url))


@app.route('/update_focus/', methods=['POST'])
def update_focus():
    user_name = session.get('user_name')
    user_id = tool.get_user_id_by_name(user_name)
    a = request.values  # 把Ajax中的数据取出来
    for i in a:
        i = eval(i)
        dict2 = i
    book_list_id = dict2['book_list_id']
    with OpenDB() as con:
        sql = "INSERT INTO `book_list`.`user_book_list` (`user_id`, `book_list_id`, `type`) VALUES ({}, {}, '2')".format(
            user_id, book_list_id)
        print(sql)
        con.execute(sql)

    return redirect(url_for('all_book_list'), 200)
@app.route('/delete_focus/', methods=['POST'])
def delete_focus():
    user_name = session.get('user_name')
    user_id = tool.get_user_id_by_name(user_name)
    a = request.values  # 把Ajax中的数据取出来
    for i in a:
        i = eval(i)
        dict2 = i
    book_list_id = dict2['book_list_id']
    with OpenDB() as con:
        sql = "DELETE FROM `book_list`.`user_book_list` WHERE `user_id` = '{}' and book_list_id='{}' and type=2".format(
            user_id, book_list_id)
        print(sql)
        con.execute(sql)

    return redirect(url_for('my_focus_list'))

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('/adminindex.html')


@app.route('/admin/user_control/', methods=['GET', 'POST'])
def user_control():
    user_information = tool.get_user_information()
    if request.method == 'POST':
        print(request.form)
        if request.form.get('update'):
            user_id = request.form['user_id']
            password = request.form['password']
            tool.update_user_password_by_user_id(user_id, password)
            return redirect(url_for('user_control'))
        if request.form.get('delete'):
            user_id = request.form['user_id']
            tool.delete_user_information_by_user_id(user_id)
            return redirect(url_for('user_control'))
        else:
            user_name = request.form['user_name']
            password = request.form['password']
            tool.insert_new_user(user_name, password)
            return redirect(url_for('user_control'))
    return render_template('/user_control.html', user_information=user_information)
@app.route('/insert_new_book/', methods=['GET', 'POST'])
def insert_new_book():
    user_name=session.get('user_name')
    if request.method=='POST' and request.form.get('word'):
        book_name = request.form['word']
        book_list = tool.search_book_name(book_name)
        return jsonify(book_list=book_list)
    if request.method=="POST" and request.form['book1']:
        type=request.form['option']
        book_list_title=request.form['book_list_title']
        book_intro=request.form['book_list_intro']
        for i in range(1,4):
            try:
                book=request.form['book{}'.format(i)]
                comment=request.form['comment{}'.format(i)]
                tool.insert_new_book_list(type,book_list_title,user_name,book_intro,book,comment)
            except:
                pass
        return redirect(url_for('index'))
    return render_template('insert_new_book.html')

@app.route('/book_list_deatil', methods=['GET', 'POST'])
def book_list_deatil():
    book_list_id=request.args.get('book_list_id')
    book_list_created_by_user_name=tool.get_create_user_name_by_book_list_id(book_list_id)
    book_list_details=tool.get_book_list_detail_information_by_book_list_id(book_list_id)

    other_book_list=tool.get_user_other_book_list_by_user_name(book_list_created_by_user_name)

    print(other_book_list)
    book_id = request.args.get('book_id')
    # 记得写1为喜欢0为不喜欢
    like_or_not = request.args.get('like_or_not')
    if like_or_not=="2":
        print("进入不喜欢")
        tool.update_book_information_by_book_id(book_id,like_or_not)
        return redirect(url_for('book_list_deatil', book_list_id=book_list_id))
    if like_or_not:
        tool.update_book_information_by_book_id(book_id, 1)
        return redirect(url_for('book_list_deatil',book_list_id=book_list_id))

    return render_template('book_list_deatil.html',book_list_details=book_list_details,other_book_list=other_book_list,book_list_id=book_list_id)
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
