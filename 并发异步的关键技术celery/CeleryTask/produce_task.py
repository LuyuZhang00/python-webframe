

# from celery_task import send_email,send_msg
#
# result = send_email.delay("yuan")
# print(result.id)
#
# result = send_msg.delay("yuan")
# print(result.id)


## 定时任务执行

from celery_task import send_email
from datetime import datetime
from datetime import timedelta
# 方式一
# v1 = datetime(2020, 3, 20, 10, 15, 00)
# print(v1)
# v2 = datetime.utcfromtimestamp(v1.timestamp())
# print(v2)
# result = send_email.apply_async(args=["egon",], eta=v2)
# print(result.id)

# 方式二
ctime = datetime.now()
# 默认用utc时间
utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())

time_delay = timedelta(seconds=10)
task_time = utc_ctime + time_delay

# 使用apply_async并设定时间
result = send_email.apply_async(args=["egon"], eta=task_time)
print(result.id)





