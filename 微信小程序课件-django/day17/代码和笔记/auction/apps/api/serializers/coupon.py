#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework import exceptions

from apps.api import models


class CouponModelSerializer(serializers.ModelSerializer):
    apply_start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    apply_stop_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    status_text = serializers.CharField(source='get_status_display')
    cover = serializers.CharField(source='auction.cover')
    remain = serializers.SerializerMethodField()

    class Meta:
        model = models.Coupon
        exclude = ['apply_start_task_id', 'apply_stop_task_id', 'deleted', 'count']

    def get_remain(self, obj):
        return obj.count - obj.apply_count


class UserCouponModelSerializer(serializers.ModelSerializer):
    remain = serializers.SerializerMethodField()

    class Meta:
        model = models.UserCoupon
        fields = ['remain', 'coupon']

    def validate_coupon(self, value):

        user_object = self.context['request'].user

        # 优惠券不存在
        if not value or value.deleted:
            raise exceptions.ValidationError('优惠券不存在')

        # 优惠券状态必须是领取中
        if value.status != 2:
            raise exceptions.ValidationError('优惠券不可领取')

        # 优惠券个数是否合法
        if (value.apply_count + 1) > value.count:
            raise exceptions.ValidationError('优惠券已领完')

        # 是否已领取优惠券
        exists = models.UserCoupon.objects.filter(user=user_object, coupon=value).exists()
        if exists:
            raise exceptions.ValidationError('已领取此优惠券')

        return value

    def get_remain(self, obj):
        return obj.coupon.count - obj.coupon.apply_count - 1


class MyUserCouponModelSerializer(serializers.ModelSerializer):
    status_text = serializers.CharField(source='get_status_display')
    coupon = serializers.CharField(source='coupon.title')
    cover = serializers.CharField(source='coupon.auction.cover')
    money = serializers.CharField(source='coupon.money')

    class Meta:
        model = models.UserCoupon
        fields = "__all__"


class ChooseCouponModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='coupon.title')
    cover = serializers.CharField(source='coupon.auction.cover')
    money = serializers.CharField(source='coupon.money')

    class Meta:
        model = models.UserCoupon
        fields = ['id', 'title', 'money', 'cover']
