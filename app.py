# 程序主页
from markupsafe import escape
from flask import Flask
from flask import url_for

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
