from flask import Flask, render_template, request

import pymysql

app = Flask(__name__)


@app.route("/add/user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")

    username = request.form.get("user")
    password = request.form.get("pwd")
    mobile = request.form.get("mobile")

    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root123", charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令
    sql = "insert into admin(username,password,mobile) values(%s,%s,%s)"
    cursor.execute(sql, [username, password, mobile])
    conn.commit()

    # 3.关闭
    cursor.close()
    conn.close()

    return "添加成功"


@app.route("/show/user")
def show_user():
    # ########## 从数据库获取所有用户信息 ###########
    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root123", charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令
    sql = "select * from admin"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    # 3.关闭
    cursor.close()
    conn.close()

    print(data_list)


    # 1.找到index.html的文件，读取所有的内容。
    # 2.找到内容中 `特殊的占位符` ，将数据替换。
    # 3.将替换完成的字符串返回给用户的浏览器。
    return render_template('show_user.html',data_list=data_list)


if __name__ == '__main__':
    app.run()
