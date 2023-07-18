import celery
import time
backend='redis://127.0.0.1:6379/1'
broker='redis://127.0.0.1:6379/2'


cel=celery.Celery('test',backend=backend,broker=broker)

@cel.task
def send_email(name):
    print("向%s发送邮件..."%name)
    time.sleep(5)
    print("向%s发送邮件完成"%name)
    return "ok"


@cel.task
def send_msg(name):

    print("向%s发送短信..."%name)
    time.sleep(5)
    print("向%s发送短信完成"%name)
    return "ok"

