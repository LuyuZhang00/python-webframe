import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demos.settings")
django.setup()

from api import models

# ########################## 创建三条根评论 ##########################
first1 = models.CommentRecord.objects.create(
    news_id=36,
    content="1",
    user_id=1,
    depth=1
)

first1_1 = models.CommentRecord.objects.create(
    news_id=36,
    content="1-1",
    user_id=6,
    reply=first1,
    depth=2,
    root=first1
)

first1_1_1 = models.CommentRecord.objects.create(
    news_id=36,
    content="1-1-1",
    user_id=10,
    reply=first1_1,
    depth=3,
    root=first1
)
first1_1_2 = models.CommentRecord.objects.create(
    news_id=36,
    content="1-1-2",
    user_id=14,
    reply=first1_1,
    depth=3,
    root=first1
)


first1_2 = models.CommentRecord.objects.create(
    news_id=36,
    content="1-2",
    user_id=8,
    reply=first1,
    depth=2,
    root=first1
)


first2 = models.CommentRecord.objects.create(
    news_id=36,
    content="2",
    user_id=3,
    depth=1
)

first3 = models.CommentRecord.objects.create(
    news_id=36,
    content="3",
    user_id=4,
    depth=1
)