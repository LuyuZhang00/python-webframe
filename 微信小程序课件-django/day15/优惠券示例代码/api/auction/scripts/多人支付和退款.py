#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import django
import uuid

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auction.settings")
django.setup()

from apps.api import models


def func(user_id, auction_id, item_id, price):
    # 1.缴纳保证金
    deposit_object = models.DepositRecord.objects.create(
        status=2,
        uid=str(uuid.uuid4()),
        deposit_type=1,
        pay_type=1,
        amount=200,
        balance=200,
        user_id=user_id,
        item_id=item_id,
        auction_id=auction_id
    )
    # 2.出价
    bid_object = models.BidRecord.objects.create(
        status=1,
        item_id=item_id,
        user_id=user_id,
        price=price
    )


if __name__ == '__main__':
    # Alex user_id=1
    func(1, 36, 18, 100)
    # 武沛齐 user_id=6
    func(6, 36, 18, 200)
