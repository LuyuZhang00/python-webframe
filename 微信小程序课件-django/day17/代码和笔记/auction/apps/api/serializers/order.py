#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework import exceptions
from django.forms import model_to_dict
from apps.api import models


class OrderModelSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(source='item.cover')
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    title = serializers.CharField(source='item.title')

    class Meta:
        model = models.Order
        exclude = ['uid', 'twenty_four_task_id', 'user', 'deposit']


class PayDepositModelSerializer(serializers.ModelSerializer):
    deposit_text = serializers.CharField(source='get_deposit_type_display')
    checked = serializers.BooleanField(default=False)

    class Meta:
        model = models.DepositRecord
        fields = ['id', 'deposit_type', 'deposit_text', 'amount', 'balance', 'checked']


class PayModelSerializer(serializers.ModelSerializer):
    user_balance = serializers.IntegerField(source='user.balance')

    auction = serializers.CharField(source='item.auction_id')

    # 拍品
    item = serializers.SerializerMethodField()

    # 保证金
    deposit = serializers.SerializerMethodField()

    # 是否有优惠券
    coupon = serializers.SerializerMethodField()

    # 支付方式
    pay_method = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        exclude = ['uid', 'twenty_four_task_id', 'user']

    def get_deposit(self, obj):
        return PayDepositModelSerializer(instance=obj.deposit).data

    def get_coupon(self, obj):
        user_object = self.context['request'].user
        exists = models.UserCoupon.objects.filter(
            user=user_object, status=1, coupon__auction=obj.item.auction_id).exists()

        context = {
            'id': None,
            'has': exists,
            'text': '请选择优惠券' if exists else '无',
            'money': 0
        }
        return context

    def get_pay_method(self, obj):
        balance = self.context['request'].user.balance
        info = {
            'selected': 1,
            'choices': [
                {'id': 1, 'text': '余额（%s）' % balance},
                {'id': 2, 'text': '微信支付'},
            ]
        }
        return info

    def get_item(self, obj):
        return {
            'title': obj.item.title,
            'cover': obj.item.cover.name,
            'uid': obj.item.uid
        }


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        exclude = ['user' ]
