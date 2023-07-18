#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
import hashlib
import time

from django.conf import settings


def md5(string):
    ha = hashlib.md5()
    ha.update(string.encode('utf-8'))
    return ha.hexdigest()


def create_uid(nickname):
    """
    生成随机字符串
    :param nickname:
    :return:
    """
    string = "{}-{}-{}".format(nickname, time.time(), str(uuid.uuid4()))
    md5_object = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    md5_object.update(string.encode('utf-8'))
    return md5_object.hexdigest()
