
#task02
import time
from celery_tasks.celery import cel
@cel.task
def send_msg(name):
    print("完成向%s发送短信任务"%name)
    time.sleep(5)
    return "短信完成！"