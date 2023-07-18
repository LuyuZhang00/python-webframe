from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from mysql_util import MysqlUtil
from passlib.hash import sha256_crypt
from functools import wraps
import time
from forms import LoginForm,ArticleForm

app = Flask(__name__) # 创建应用
app.config['SECRET_KEY'] = 'mrsoft'

# 首页
@app.route('/')
def index():
    db = MysqlUtil() # 实例化数据库操作类
    count = 3 # 每页显示数量
    page = request.args.get('page') # 获取当前页码
    if page is None: # 默认设置页码为1
        page = 1
    # 分页查询
    # 从article表中筛选5条数据，并根据日期降序排序
    sql = f'SELECT * FROM articles  ORDER BY create_date DESC LIMIT {(int(page)-1)*count},{count}'
    articles = db.fetchall(sql) # 获取多条记录
    # 遍历文章数据
    return render_template('home.html', articles=articles,page=int(page)) # 渲染模板

# 关于我们
@app.route('/about')
def about():
    return render_template('about.html') # 渲染模板

# 笔记详情
@app.route('/article/<string:id>/')
def article(id):
    db = MysqlUtil() # 实例化数据库操作类
    sql = "SELECT * FROM articles WHERE id = '%s'" % (id) # 根据ID查找笔记
    article = db.fetchone(sql) # 获取一条记录
    return render_template('article.html', article=article) # 渲染模板

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" in session:  # 如果已经登录，则直接跳转到控制台
        return redirect(url_for("dashboard"))

    form = LoginForm(request.form)  # 实例化表单类
    if form.validate_on_submit():   # 如果提交表单，并字段验证通过
        # 从表单中获取字段
        username = request.form['username']
        password_candidate = request.form['password']
        sql = "SELECT * FROM users  WHERE username = '%s'" % (username) # 根据用户名查找user表中记录
        db = MysqlUtil() # 实例化数据库操作类
        result = db.fetchone(sql) # 获取一条记录
        password = result['password']  # 用户填写的密码
        # 对比用户填写的密码和数据库中记录密码是否一致
        if sha256_crypt.verify(password_candidate, password): # 调用verify方法验证，如果为真，验证通过
            # 写入session
            session['logged_in'] = True
            session['username'] = username
            flash('登录成功！', 'success') # 闪存信息
            return redirect(url_for('dashboard')) # 跳转到控制台
        else:  # 如果密码错误
            flash('用户名和密码不匹配！', 'danger')  # 闪存信息

    return render_template('login.html',form=form)

# 如果用户已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:     # 判断用户是否登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:                          # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login'))
    return wrap

# 退出
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('您已成功退出', 'success')   # 闪存信息
    return redirect(url_for('login')) # 跳转到登录页面

# 控制台
@app.route('/dashboard')
@is_logged_in
def dashboard():
    db = MysqlUtil() # 实例化数据库操作类
    sql = "SELECT * FROM articles WHERE author = '%s' ORDER BY create_date DESC" % (session['username']) # 根据用户名查找用户笔记信息
    result = db.fetchall(sql) # 查找所有笔记
    if result: # 如果笔记存在，赋值给articles变量
        return render_template('dashboard.html', articles=result)
    else:      # 如果笔记不存在，提示暂无笔记
        msg = '暂无笔记信息'
        return render_template('dashboard.html', msg=msg)

# 添加笔记
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form) # 实例化ArticleForm表单类
    if request.method == 'POST' and form.validate(): # 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        title = form.title.data
        content = form.content.data
        author = session['username']
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db = MysqlUtil() # 实例化数据库操作类
        sql = "INSERT INTO articles(title,content,author,create_date) \
               VALUES ('%s', '%s', '%s','%s')" % (title,content,author,create_date) # 插入数据的SQL语句
        db.insert(sql)
        flash('创建成功', 'success') # 闪存信息
        return redirect(url_for('dashboard'))               # 跳转到控制台
    return render_template('add_article.html', form=form)   # 渲染模板


# 编辑笔记
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    db = MysqlUtil()  # 实例化数据库操作类
    fetch_sql = "SELECT * FROM articles WHERE id = '%s' and author = '%s'" % (id,session['username']) # 根据笔记ID查找笔记信息
    article = db.fetchone(fetch_sql) # 查找一条记录
    # 检测笔记不存在的情况
    if not article:
        flash('ID错误', 'danger') # 闪存信息
        return redirect(url_for('dashboard'))
    # 获取表单
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate(): # 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        title = request.form['title']
        content = request.form['content']
        update_sql = "UPDATE articles SET title='%s', content='%s' WHERE id='%s' and author = '%s'" % (title, content, id,session['username'])
        db = MysqlUtil() # 实例化数据库操作类
        db.update(update_sql) # 更新数据的SQL语句
        flash('更改成功', 'success') # 闪存信息
        return redirect(url_for('dashboard')) # 跳转到控制台

    # 从数据库中获取表单字段的值
    form.title.data = article['title']
    form.content.data = article['content']
    return render_template('edit_article.html', form=form) # 渲染模板

# 删除笔记
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    db = MysqlUtil() # 实例化数据库操作类
    sql = "DELETE FROM articles WHERE id = '%s' and author = '%s'" % (id,session['username']) # 执行删除笔记的SQL语句
    db.delete(sql) # 删除数据库
    flash('删除成功', 'success') # 闪存信息
    return redirect(url_for('dashboard')) # 跳转到控制台

# 404页面
@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("/404.html"), 404


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
