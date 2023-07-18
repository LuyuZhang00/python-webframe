#task01
import time
from celery_tasks.celery import cel
from celery_once import QueueOnce


@cel.task
def send_email(res):
    print("完成向%s发送邮件任务"%res)
    time.sleep(5)
    return "邮件完成！"