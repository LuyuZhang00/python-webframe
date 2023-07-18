#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auction.settings")
django.setup()

from apps.api import models

result = models.Topic.objects.bulk_create([
    models.Topic(title='春运'),
    models.Topic(title='年终奖'),
])
print(result)
