#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.generics import ListAPIView, CreateAPIView
from apps.api import models
from apps.api.serializers.coupon import CouponModelSerializer, UserCouponModelSerializer, MyUserCouponModelSerializer, \
    ChooseCouponModelSerializer
from utils.auth import UserAuthentication
from django.db import transaction
from rest_framework import exceptions
from rest_framework import status
from collections import OrderedDict


class CouponView(ListAPIView):
    queryset = models.Coupon.objects.filter(deleted=False).exclude(status=1).order_by('-id')
    serializer_class = CouponModelSerializer


class UserCouponView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthentication, ]

    def perform_create(self, serializer):
        with transaction.atomic():
            coupon_object = models.Coupon.objects.filter(
                id=serializer.validated_data['coupon'].id).select_for_update().first()
            if (coupon_object.apply_count + 1) > coupon_object.count:
                raise exceptions.ValidationError('优惠券已领完')
            serializer.save(user=self.request.user)
            coupon_object.apply_count += 1
            coupon_object.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCouponModelSerializer
        return MyUserCouponModelSerializer

    def get_queryset(self):
        return models.UserCoupon.objects.filter(user=self.request.user)

    def list(self, *args, **kwargs):
        response = super().list(*args, **kwargs)  # [{},{},{}]
        if response.status_code != status.HTTP_200_OK:
            return response
        """
        {
            1:{text:'未使用',child:[..]}
            2:{text:'已使用',child:[...]}
            3:{text:'已过期',child:[...]}
        }
        """
        status_dict = OrderedDict()
        for item in models.UserCoupon.status_choices:
            status_dict[item[0]] = {'text': item[1], 'child': []}

        for row in response.data:
            status_dict[row['status']]['child'].append(row)

        response.data = status_dict
        return response


class ChooseCouponView(ListAPIView):
    """ 支付页面 选择优惠券 """
    authentication_classes = [UserAuthentication, ]
    serializer_class = ChooseCouponModelSerializer

    def get_queryset(self):
        auction = self.request.query_params.get('auction')
        # return models.UserCoupon.objects.filter(user=self.request.user, coupon__auction_id=auction, status=1)
        return models.UserCoupon.objects.all()
