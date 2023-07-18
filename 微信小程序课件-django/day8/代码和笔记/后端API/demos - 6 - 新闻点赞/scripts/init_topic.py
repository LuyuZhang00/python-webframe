

import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件的路径写到 DJANGO_SETTINGS_MODULE 环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demos.settings")
django.setup()

from api import models
models.Topic.objects.create(title="春运")
models.Topic.objects.create(title="火车票")