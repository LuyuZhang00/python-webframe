from celery import Celery

app = Celery('tasks', broker='redis://192.168.16.86:6379', backend='redis://192.168.16.86:6379')
app.conf.timezone = 'Asia/Shanghai'

@app.task
def x1(x, y):
    return x + y


@app.task
def x2(x, y):
    return x - y