# 程序主页
from flask_login import LoginManager
import click
from flask import Flask, render_template
from markupsafe import escape
from flask import Flask
from flask import url_for
from flask import request, url_for, redirect, flash
# Flask 会在请求触发后把请求信息放到 request 对象里，你可以从 flask 包导入它：
import os
import sys
# from foo_orm import Model, Column, String

from werkzeug.security import generate_password_hash, check_password_hash
# 使用Flask依赖Werkzeug内置的用于生成和验证密码散列值的函数

from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

from flask_login import UserMixin
# 从 flask 包导入 Flask 类，通过实例化这个类，创建一个程序对象 app
from flask_login import login_required, logout_user

app = Flask(__name__)

# 使用 app.route() 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个 URL 的时候，
# 就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：


@app.route('/home')  # 视图函数URL改变，可绑定多个URL
def hello():
    return 'Welcome to My Watchlist! <h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# 整个请求的处理过程如下所示：

# 1.当用户在浏览器地址栏访问这个地址，在这里即 http://localhost:5000/
# 2.服务器解析请求，发现请求 URL 匹配的 URL 规则是 /，因此调用对应的处理函数 hello()
# 3.获取 hello() 函数的返回值，处理后返回给客户端（浏览器）
# 4.浏览器接受响应，将其显示在窗口上

# 手动启用调试模式
# set FLASK_ENV=developm


# 定义变量


@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'  # escape() 函数对 name 变量进行转义处理


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


# 定义虚拟数据填充页面内容
name = 'Emroy Can'
books = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

# 渲染主页模板
# 返回渲染好的模板作为响应

# ...


# @app.route('/')
# def index():
#     # 设置了数据库，负责显示主页的 index 可以从数据库里读取真实的数据：
#     user = User.query.first()  # 读取用户记录
#     books = Book.query.all()  # 读取所有电影记录
#     return render_template('index.html', user=user, books=books)
#     # return render_template('index.html', name=name, books=books)
#     # 左边的 movies 是模板中使用的变量名称，右边的 movies 则是该变量指向的实际对象。
#     # 这里传入模板的 name 是字符串，movies 是列表，
#     # 模板里使用的Python 数据结构也可以传入元组、字典、函数等。
#     # render_template() 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句


# db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app

# 设置数据库URL sqlite:////数据库文件的绝对地址  app.root_path返回程序实例所在模块的路径（目前项目根目录）
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')


WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'


app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(
        app.root_path, 'data.db')  # 设置数据库URL  SQLALCHEMY_DATABASE_URI 变量来告诉 SQLAlchemy 数据库连接地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app


# 创建数据库模型 SQL炼金术
# 存储用户信息的User模型类，为新增用户认证，添加username字段：存储登录所需用户名；password_hash字段：密码散列值
class User(db.Model, UserMixin):  # 表名user(自动生成) 单个单词转小写 多个小写下划线分割
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))   # 名字
# 表的字段（列）由db.Column类的实例表示，字段的类型通过Column类的构造方法的第一个参数传入
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接收密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保存到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

# 因为模型表结构发生变化，需重新生成数据库（会清空数据）：
# flask initdb --drop


# 编写命令创建管理员账户
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')

# click.option()装饰器设置的两个选项分别用来接受输入用户名和密码。执行flask命令创建


class Book(db.Model):  # 表名book
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 书名
    year = db.Column(db.String(4))  # 年份

# hrserver 数据test


class DataSetModel(db.Model):

    __tablename__ = 'dataset'
    id = db.Column(db.Integer, name='id', comment='id', primary_key=True)
    name = db.Column(db.String(100), name='name', comment='名称')
    type = db.Column(db.Integer, name='type',
                     comment='类型(0:文件夹, 1:sql数据集, 2:excel数据集)')


class DataSetSql(db.Model):
    """
    sql数据集内容
    """
    __tablename__ = 'dataset_sql'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, name='id', comment='id', primary_key=True)
    dataset_id = db.Column(db.Integer, name='dataset_id', comment='数据集id')
    datasource_id = db.Column(
        db.Integer, name='datasource_id', comment='数据源id')
    table = db.Column(db.String(100), name='table', comment='表或视图名')
    sql = db.Column(db.Text, name='sql', comment='自定义sql语句')


class DataSetFile(db.Model):
    """
    excel数据集内容
    """
    __tablename__ = 'dataset_excel'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, name='id', comment='id', primary_key=True)
    dataset_id = db.Column(db.Integer, name='dataset_id', comment='数据集id')
    file_path = db.Column(db.String(1024), name='file_path', comment='文件路径')
    load_mode = db.Column(db.Integer, name='load_mode',
                          comment='加载方式, 0 - 源表, 1 - 生成逆透视表', default=0)
    start_line = db.Column(db.Integer, name='start_line',
                           comment='起始行', default=1)
    header = db.Column(db.Integer, name='header',
                       comment='表头, 0 - 自动, 1 - 第一行, 2 - 无', default=0)
    delete_invalid = db.Column(
        db.Boolean, name='delete_invalid', comment='删除无效行', default=False)
    worksheet = db.Column(db.String(1024), name='worksheet')
    code_type = db.Column(db.String(1024), name='code_type')
    delimiter = db.Column(db.String(1024), name='delimiter')


# 模型类编写限制：
# 模型类的编写有一些限制：
# 模型类要声明继承 db.Model。
# 每一个类属性（字段）要实例化 db.Column，传入的参数为字段的类型，下面的表格列出了常用的字段类。
# 在 db.Column() 中添加额外的选项（参数）可以对字段进行设置。比如，primary_key 设置当前字段是否为主键。除此之外，常用的选项还有 nullable（布尔值，是否允许为空值）、index（布尔值，是否设置索引）、unique（布尔值，是否允许重复值）、default（设置默认值）等。


# python shell创建数据库表 `flask shell`  `from app import db` `db.create_all()`
# 改动模型类需先db.drop_all()删除表 然后重新创建。

# 如果不一并删除所有数据，不破坏数据库内的数据的前提下变更表的结果，需使用数据库迁移工具 Flask-Migrate扩展


# 自定义命令来自动执行创建数据库表操作：flask initdb 命令就可以创建数据库表： 使用 --drop 选项可以删除表后重新创建：
@app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

# 数据库操作 CRUD
# SQLAIchemy使用数据库会话来管理数据库操作，这里的数据库会话也称事务（transaction)
# Flask-SQLAIchemy会自动帮我们创建会话，可以通过db.session属性获取。
# 会话代表一个临时存储区，只有调用commit()方法改动才会被提交到数据库，这确保了数据提交的一致性。支持回滚操作，rollback(),撤销改动未提交。


# flask shell向数据库中添加记录
# 1. 创建python对象(实例化模型类)作为一条记录
# 2. 添加新创建的记录到数据库会话 使用关键字参数传入字段数据 db.Model基类会提供构造函数赋值对应的类属性。
# 3. 提交数据库会话
# >>> from app import User, Book  # 导入模型类
# >>> user = User(name='Emroy')  # 创建一个 User 记录
# >>> m1 = Book(title='Leon', year='1994')  # 创建一个 Book记录
# >>> m2 = Book(title='Mahjong', year='1996')  # 再创建一个 Book记录
# >>> db.session.add(user)  # 把新创建的记录添加到数据库会话
# >>> db.session.add(b1)
# >>> db.session.add(b2)
# >>> db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
# 实例化模型类的时候，我们并没有传入 id 字段（主键），因为 SQLAlchemy 会自动处理这个字段。
# db.session.add() 调用是将改动添加进数据库会话（一个临时区域）中
# db.session.commit() 很重要，只有调用了这一行才会真正把记录提交进数据库


# 读取
# 通过对模型类的query属性调用可选的过滤方法和查询方法可以获取到对应的单个或多记录
# 记录以模型类实例的形式表示
# 查询语句的格式如下：
# <模型类>.query.<过滤方法（可选）>.<查询方法>

# 过滤方法	说明
# filter()	使用指定的规则过滤记录，返回新产生的查询对象
# filter_by()	使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象
# order_by()	根据指定条件对记录进行排序，返回新产生的查询对象
# group_by()	根据指定条件对记录进行分组，返回新产生的查询对象


# 常用的查询方法：

# 查询方法	说明
# all()	    返回包含所有查询记录的列表
# first()	返回查询的第一条记录，如果未找到，则返回 None
# get(id)	传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 None
# count()	返回查询结果的数量
# first_or_404()	返回查询的第一条记录，如果未找到，则返回 404 错误响应
# get_or_404(id)	传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 404 错误响应
# paginate()	返回一个 Pagination 对象，可以对记录进行分页处理


# 生成虚拟数据 编写命令函数把虚拟数据添加到数据库
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Emroy'
    books = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for b in books:
        book = Book(title=b['title'], year=b['year'])
        db.session.add(book)

    db.session.commit()
    click.echo('Done.Add fake data in database')


@app.cli.command()
def forge1():
    db.create_all()
    # 全局的两个变量移动到这个函数内
    datasetmodels = [{'name': 'sql', 'type': '1'},
                     {'name': 'csv', 'type': '2'}]
    datasetsqls = [{'dataset_id': '87',
                    'table': 'data_studio_miner/table/miner_dig'}, {'dataset_id': '89',
                                                                    'table': 'data_studio_miner/table/miner'}]
    datasetexcels = [
        {'file_path': 'D:\study\416007000.csv', 'dataset_id': '86'}, {'file_path': 'D:\study\112.xlsx', 'dataset_id': '67'}]
    for m in datasetmodels:
        datasetmodel = DataSetModel(name=m['name'], type=m['type'])
        db.session.add(datasetmodel)
    for s in datasetsqls:
        datasetsql = DataSetSql(dataset_id=s['dataset_id'], table=s['table'])
        db.session.add(datasetsql)
    for e in datasetexcels:
        datasetexcel = DataSetFile(
            file_path=e['file_path'], dataset_id=e['dataset_id'])
        db.session.add(datasetexcel)
    db.session.commit()
    click.echo('Add fake data in dataset')


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码

# 模板上下文处理函数


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# # @app.route('/')
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     books = Book.query.all()
#     return render_template('index.html', books=books)

# 因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据 request.form 是一个特殊的字典，用表单字段的 name 属性值可以获取用户填入的对应数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        book = Book(title=title, year=year)  # 创建记录
        db.session.add(book)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        # 显示成功创建的提示 get_flashed_messages() 函数则用来在模板中获取提示消息
        flash('Item created.')
        return redirect(url_for('index'))  # 重定向回主页

    books = Book.query.all()
    return render_template('index.html', books=books)


# 编辑条目

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    # book_id 变量是书条目记录在数据库中的主键值，
    # 这个值用来在视图函数里查询到对应的书记录。查询的时候，我们使用了 get_or_404() 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', book_id=book_id))  # 重定向回对应的编辑页面

        book.title = title  # 更新标题
        book.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', book=book)  # 传入被编辑的电影记录


# 删除条目
@app.route('/book/delete/<int:book_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(book_id):  # 不涉及数据传递，创建删除视图函数
    book = Book.query.get_or_404(book_id)  # 获取书记录
    db.session.delete(book)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
# 为安全考虑，一般使用POST请求提交删除请求，即使用表单来实现（而不是创建删除连接）


# 使用Flask-Login实现用户认证需要的各类功能函数，我们将使用它来实现程序的用户认证

login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户I的作为参数
    user = User.query.get(int(user_id))  # 用ID作为User模型类的主键查询对应的用户
    return user  # 返回用户对象
# Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录。

# 另一个步骤是让存储用户的 User 模型类继承 Flask-Login 提供的 UserMixin 类：
# 继承之后会让User类拥有几个用于判断认证状态的属性和方法，其中最常用的是 is_authenticated 属性：如果当前用户已经登录，那么 current_user.is_authenticated 会返回 True， 否则返回 False。
# 有了 current_user 变量和这几个验证方法和属性，我们可以很轻松的判断当前用户的认证状态。

# 用于显示登录页面和处理登录表单提交请求的视图函数：


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向导主页

        flash('Invalid username or password')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


# 登出
@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页
