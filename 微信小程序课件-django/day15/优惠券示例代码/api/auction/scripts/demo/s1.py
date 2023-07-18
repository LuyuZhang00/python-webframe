#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from celery import Celery, shared_task


@shared_task
def x2(x):
    return x


@shared_task
def x1(x, y):
    return x + y


app1 = Celery('tasks1', broker='redis://10.211.55.25:6379', backend='redis://10.211.55.25:6379')
