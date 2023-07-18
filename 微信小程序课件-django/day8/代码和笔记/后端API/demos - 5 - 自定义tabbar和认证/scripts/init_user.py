import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件的路径写到 DJANGO_SETTINGS_MODULE 环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demos.settings")
django.setup()

from api import models
for i in range(20):
    models.UserInfo.objects.create(
        telephone='1513125555',
        nickname='大卫-{0}'.format(i),
        avatar='https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png'
    )