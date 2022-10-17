# 程序主页
import click
from flask import Flask, render_template
from markupsafe import escape
from flask import Flask
from flask import url_for

import os
import sys

from flask_sqlalchemy import SQLAlchemy  # 导入扩展类


# 从 flask 包导入 Flask 类，通过实例化这个类，创建一个程序对象 app

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


@app.route('/')
def index():
    # 设置了数据库，负责显示主页的 index 可以从数据库里读取真实的数据：
    user = User.query.first()  # 读取用户记录
    books = Book.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, books=books)
    # return render_template('index.html', name=name, books=books)
    # 左边的 movies 是模板中使用的变量名称，右边的 movies 则是该变量指向的实际对象。
    # 这里传入模板的 name 是字符串，movies 是列表，
    # 模板里使用的Python 数据结构也可以传入元组、字典、函数等。
    # render_template() 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句


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
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app


# 创建数据库模型
class User(db.Model):  # 表名user(自动生成)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))   # 名字


class Book(db.Model):  # 表名book
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 书名
    year = db.Column(db.String(4))  # 年份

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


# flask shell向数据库中添加记录
# >>> from app import User, Movie  # 导入模型类
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
# all()	返回包含所有查询记录的列表
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
    click.echo('Done.')
