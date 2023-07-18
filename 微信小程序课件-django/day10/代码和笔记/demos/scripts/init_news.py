"""
初始化动态表，在动态表中添加一些数据，方便操作
"""
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demos.settings")
django.setup()

from api import models

for i in range(1,37):
    news_object = models.News.objects.create(
        cover="https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        content="还有{0}天就放假".format(i),
        topic_id=1,
        user_id=1
    )

    models.NewsDetail.objects.create(
        key="08a9daei1578736867828.png",
        cos_path="https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        news=news_object
    )

    models.NewsDetail.objects.create(
        key="0d3q0evq1578906084254.jpg",
        cos_path="https://mini-1251317460.cos.ap-chengdu.myqcloud.com/0d3q0evq1578906084254.jpg",
        news=news_object
    )