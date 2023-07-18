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


def first_depth_commont():
    models.CommentRecord.objects.bulk_create([
        models.CommentRecord(
            news_id=1,
            content='我来了',
            user_id=1,
            depth=1
        ),
        models.CommentRecord(
            news_id=1,
            content='天王盖地虎',
            user_id=1,
            depth=1
        ),
        models.CommentRecord(
            news_id=1,
            content='今天天气不错',
            user_id=1,
            depth=1
        ),
        models.CommentRecord(
            news_id=1,
            content='傻吊',
            user_id=1,
            depth=1
        )
    ])


def second_depth_comment():
    models.CommentRecord.objects.bulk_create([
        models.CommentRecord(
            news_id=1,
            content='我来了',
            user_id=1,
            depth=2,
            reply_id=1
        ),
        models.CommentRecord(
            news_id=1,
            content='天王盖地虎',
            user_id=1,
            depth=2,
            reply_id=1
        ),
        models.CommentRecord(
            news_id=1,
            content='今天天气不错',
            user_id=1,
            depth=2,
            reply_id=2
        ),
        models.CommentRecord(
            news_id=1,
            content='傻吊',
            user_id=1,
            depth=2,
            reply_id=3
        )
    ])


if __name__ == '__main__':
    # first_depth_commont()
    # second_depth_comment()
    pass