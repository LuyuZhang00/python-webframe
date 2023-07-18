from flask import Flask, render_template

app = Flask(__name__)


# 创建了网址 /show/info 和 函数index 的对应关系
# 以后用户在浏览器上访问 /show/info，网站自动执行 index
@app.route("/show/info")
def index():
    # return "中国联通"
    # return "中<h1>国</h1><span style='color:red;'>联通</span>"
    # Flask内部会自动打开这个文件，并读取内容，将内容给用户返回。
    # 默认：去当前项目目录的 templates 文件夹中找。
    return render_template("index.html")


@app.route("/get/news")
def get_news():
    return render_template("get_news.html")


@app.route("/goods/list")
def goods_list():
    return render_template("goods_list.html")


@app.route("/user/list")
def user_list():
    return render_template("user_list.html")

@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run()
