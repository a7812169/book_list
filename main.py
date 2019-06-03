from flask import Flask
import json
from flask import request, flash, url_for, redirect
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
        print(user, password, confirm_password)
        if password == confirm_password:
            pass
        else:
            flash('密码不一致')
        with OpenDB() as con:
            sql = 'select user from user_information where user="{}"'.format(user)
            con.execute(sql)
            if len(con.fetchall()) > 0:
                print(con.fetchall())
                flash('注册成功')
            else:
                sql = 'insert into user_information(`user`,`password`)values("{}","{}")'.format(user, password)
                try:
                    con.execute(sql)
                except:
                    print('发生位置错误，无法插入')
        return render_template('zhuceye.html')
    else:
        return render_template('zhuceye.html')


# 入口首页
@app.route('/index', methods=['POST', 'GET'])
def index():
    like_book_ssid = request.args.get('ssid')
    user_name = session.get('user_name')
    if request.args.get('type'):
        book_list_id = request.args.get('book_list_id')
        print(book_list_id)
        user_id=tool.get_user_id_by_name(user_name)
        print(user_id)
        tool.update_like_number_by_user_id(user_id,book_list_id)
    if like_book_ssid:
        with OpenDB() as con:
            sql = 'select user from user_information where user="{}"'.format(user_name)
            con.execute(sql)
    if user_name:
        user_id = tool.get_user_id_by_name(user_name)
    # todo 这里以后需要写个sql 转换ssid
    new_list = tool.get_list("new", user_id=None)
    # 最新漂流
    elite_list = tool.get_list("elite", user_id=None)
    # 精品书单
    your_like_list = tool.get_list("you_like", user_id=None)
    comment_list = tool.get_user_comment()
    # comment_list_by_book=tool.get_comment_by_book_id()
    return render_template('index.html', new_list=new_list, elite_list=elite_list, your_like_list=your_like_list,
                           comment_list=comment_list,
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

    book_list = book_list[data:data2]
    return render_template('all_book_list.html', book_list=book_list, user_focus_list=user_focus_list,
                           total_page=list(range(total_page)), now_page=int(now_page))


@app.route('/my_focus_list', methods=['POST', 'GET'])
def my_focus_list():
    user_name = request.args.get('user_name')
    user_id = tool.get_user_id_by_name(user_name)


# 图书分类
@app.route('/category', methods=['POST', 'GET'])
def category():
    user_name = session.get('user_name')
    book_type = request.args.get('book_type')
    print(book_type)
    from tool import get_book_infomation_by_type
    total_book_list = get_book_infomation_by_type(book_type)

    max_page = len(total_book_list) / 10
    page = request.args.get('page')
    if not page:
        page = 1
    this_page_book_list = total_book_list[page * 10:(page + 1) * 10]
    return render_template('category.html', this_page_book_list=this_page_book_list, book_type=book_type, now_page=page,
                           max_page=max_page)


# 选择点击喜好
@app.route('/category/like_or_no_like', methods=['GET'])
def like_or_like():
    user_name = request.args.get('user_name')
    book_id = request.args.get('book_id')
    # 记得写1为喜欢0为不喜欢
    like_or_no = request.args.get('like_or_no')
    if like_or_no:
        tool.update_book_information_by_book_id(book_id, like_or_no)
    else:
        tool.update_book_information_by_book_id(book_id, like_or_no)
    return redirect(category)


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
    print(book_list_id)
    print(user_id)
    with OpenDB() as con:
        sql = "INSERT INTO `book_list`.`user_book_list` (`user_id`, `book_list_id`, `type`) VALUES ({}, {}, '2')".format(
            user_id, book_list_id)
        print(sql)
        con.execute(sql)

    return redirect(url_for('all_book_list'), 200)
@app.route('/admin',methods=['GET'])
def admin():
    return render_template('/adminindex.html')
@app.route('/admin/user_control/',methods=['GET','POST'])
def user_control():
    user_information=tool.get_user_information()
    if request.method=='POST':
        print(request.form)
        if request.form.get('update'):
            user_id=request.form['user_id']
            password = request.form['password']
            tool.update_user_password_by_user_id(user_id,password)
            return redirect(url_for('user_control'))
        if request.form.get('delete'):
            user_id=request.form['user_id']
            tool.delete_user_information_by_user_id(user_id)
            return redirect(url_for('user_control'))
        else:
            user_name=request.form['user_name']
            password=request.form['password']
            tool.insert_new_user(user_name,password)
            return redirect(url_for('user_control'))
    return render_template('/user_control.html',user_information=user_information)
if __name__ == '__main__':


    app.run()
