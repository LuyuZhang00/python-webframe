from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index')
def index():
    # 目前写死；读取文件
    users = ["吴阳军", "弄援军", "可以的", "张杰斌"]

    # 1.找到index.html的文件，读取所有的内容。
    # 2.找到内容中 `特殊的占位符` ，将数据替换。
    # 3.将替换完成的字符串返回给用户的浏览器。
    return render_template("index.html", title="中国联通", data_list=users)


if __name__ == '__main__':
    app.run()
