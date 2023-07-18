#!/usr/bin/env python
# -*- coding:utf-8 -*-

from celery import shared_task


@shared_task
def preview_status_task(auction_id):
    return 999
