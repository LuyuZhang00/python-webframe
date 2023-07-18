#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers

from .. import models


class BidModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.nickname', read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = models.BidRecord
        exclude = ['user', 'status', ]

    def validate_item(self, value):
        """ 验证是否还正在拍卖"""
        item_id = self.initial_data.get('item')
        exists = models.AuctionItem.objects.filter(id=item_id, status=3).exists()
        if not exists:
            raise exceptions.ValidationError('拍卖商品不存在或已成交')
        return value

    def validate_price(self, value):
        """ 验证价格
        1. 比最大的要大
        2. 是单元的倍数
        """
        from django.db.models import Max
        item_id = self.initial_data.get('item')
        item_object = models.AuctionItem.objects.filter(id=item_id).first()
        if value < item_object.start_price:
            raise exceptions.ValidationError('出价不能低于低价')
        result = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price'))
        if not result['max_price']:
            return value
        if value <= result['max_price']:
            raise exceptions.ValidationError('已有出价更高者，请调整出价')
        return value
