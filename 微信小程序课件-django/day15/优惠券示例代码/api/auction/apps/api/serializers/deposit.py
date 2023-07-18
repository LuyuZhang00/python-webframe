#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework import exceptions

from apps.api import models


class PayDepositSerializer(serializers.Serializer):
    auction_id = serializers.IntegerField(label='拍卖ID')
    item_id = serializers.IntegerField(label='拍品ID')
    deposit_type = serializers.IntegerField(label='保证金类型')
    amount = serializers.IntegerField(label='付款金额')
    pay_type = serializers.IntegerField(label='支付方式')

    def validate_auction_id(self, value):
        """ 检查是否已支付全场保证金 """
        user_object = self.context['request'].user
        exists = models.DepositRecord.objects.filter(user=user_object, auction_id=value, item__isnull=True,
                                                     status=2).exists()
        if exists:
            raise exceptions.ValidationError(detail='已支付过全场保证金')
        return value

    def validate_item_id(self, value):
        """ 检查是否已支付单品保证金 """
        user_object = self.context['request'].user
        exists = models.DepositRecord.objects.filter(user=user_object, item__id=value, status=2).exists()
        if exists:
            raise exceptions.ValidationError(detail='已支付此单品保证金')
        return value

    def validate_deposit_type(self, value):
        # 单品保证金
        if value == 1:
            return value
        # 全场保证金，已支付过其他单品保证金，则不能再支付全场保证金。
        if value == 2:
            user_object = self.context['request'].user
            auction_id = self.initial_data.get('auction_id')
            exists = models.DepositRecord.objects.filter(user=user_object, auction_id=auction_id, status=2).exists()
            if exists:
                raise exceptions.ValidationError(detail='已支付其他单品保证金，无法再支付全场保证金')
            return value
        raise exceptions.ValidationError(detail='保证金类型错误')

    def validate_amount(self, value):
        deposit_type = self.initial_data.get('deposit_type')

        # 单品保证金
        if deposit_type == 1:
            item_id = self.initial_data.get('item_id')
            exists = models.AuctionItem.objects.filter(id=item_id, deposit=value).exists()
            if not exists:
                raise exceptions.ValidationError(detail='保证金金额错误')
            return value

        # 全场保证金
        if deposit_type == 2:
            auction_id = self.initial_data.get('auction_id')
            exists = models.Auction.objects.filter(id=auction_id, deposit=value).exists()
            if not exists:
                raise exceptions.ValidationError(detail='保证金金额错误')
            return value

    def validate_pay_type(self, value):
        # 微信支付
        if value == 1:
            return value

        # 余额支付，余额是否充足。
        if value == 2:
            user_object = self.context['request'].user
            amount = self.initial_data.get('amount')
            if user_object.balance < amount:
                raise exceptions.ValidationError(detail='余额不足')
            return value

        raise exceptions.ValidationError(detail='支付方式错误')


class AuctionDepositModelSerializer(serializers.ModelSerializer):
    deposit = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    cover = serializers.CharField()

    class Meta:
        model = models.AuctionItem
        fields = ['id', 'auction_id', 'title', 'cover', 'start_price', 'reserve_price', 'highest_price', 'deposit',
                  'balance']

    def get_deposit(self, obj):
        # 展示单品保证金和全场保证金
        #   1. 如果已支付过单品保证金，则不能再支付全场保证金。
        #   2. 如果已支付过全场保证经，则无需再支付保证金
        context = {
            'selected': 1,
            'money': obj.deposit,
            'list': [
                {'id': 1, 'money': obj.deposit, 'text': '单品保证金', 'checked': True},
                {'id': 2, 'money': obj.auction.deposit, 'text': '全场保证金'}
            ]
        }
        return context

    def get_balance(self, obj):
        user_object = self.context['request'].user
        return user_object.balance
