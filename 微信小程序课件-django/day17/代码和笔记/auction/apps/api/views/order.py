#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
from rest_framework.views import APIView
from collections import OrderedDict
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from apps.api import models
from utils.auth import UserAuthentication
from django.db import transaction
from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from apps.api.serializers.order import OrderModelSerializer, PayModelSerializer, AddressModelSerializer


class OrderView(ListAPIView):
    """ 订单接口 """
    authentication_classes = [UserAuthentication, ]
    # queryset = models.Order.objects.all().order_by('id')
    serializer_class = OrderModelSerializer

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user).order_by('id')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return response

        info = OrderedDict()
        for item in models.Order.status_choices:
            info[item[0]] = {'text': item[1], 'child': []}

        for item in response.data:
            info[item['status']]['child'].append(item)
        response.data = info
        return response


class PayView(RetrieveAPIView):
    authentication_classes = [UserAuthentication, ]
    # queryset = models.Order.objects.filter(status=1)
    serializer_class = PayModelSerializer

    def get_queryset(self):
        return models.Order.objects.filter(status=1,user=self.request.user)


class PayNowView(APIView):
    """ 立即支付 """
    authentication_classes = [UserAuthentication, ]

    def post(self, request, *args, **kwargs):
        print(request.data)
        # 1. 接收用户请求数据
        """
            {
                order_id: 1,
                coupon_id: 9, # 可以为空
                use_deposit: True/False # ,
                address_id: 1,
                real_pay: 100,
                pay_type: 1微信/2余额,
                
            }
        """

        order_id = request.data['order_id']
        coupon_id = request.data['coupon_id']
        use_deposit = request.data['use_deposit']
        address_id = request.data['address_id']
        real_pay = request.data['real_pay']
        pay_type = request.data['pay_type']

        deposit_deduct_object = None
        deposit_refund_object = None
        coupon_object = None

        # 2. 数据校验
        address_object = models.Address.objects.filter(user=request.user, id=address_id).first()
        if not address_object:
            raise exceptions.ValidationError('地址不存在')

        with transaction.atomic():
            # ## 2.1 订单是否合法？是否已经支付？
            order_object = models.Order.objects.filter(id=order_id, status=1,
                                                       user=request.user).select_for_update().first()
            if not order_object:
                raise exceptions.ValidationError('订单不存在')

            # 原价
            origin_price = order_object.price

            # 应该支付的价格
            real_price = order_object.price

            # ## 2.2 是否用优惠券
            if not coupon_id:
                # 不用优惠券
                pass
            else:
                # 用优惠券
                coupon_object = models.UserCoupon.objects.filter(id=coupon_id, user=request.user, status=1).first()
                if not coupon_object:
                    raise exceptions.ValidationError('优惠券不存在')

                if coupon_object.coupon.money > origin_price:
                    real_price = 0
                else:
                    real_price = origin_price - coupon_object.coupon.money

                # ---> bug: 优惠券更新为已使用 ? <----
                coupon_object.status = 2
                coupon_object.order = order_object

            # ## 2.3 是否用保证金？
            if not use_deposit:
                # 用户不用保证金抵扣，自己还有保证金
                # 如果原来交的是单品保证金，直接退
                # 如果来交的是全场保证金，直接退（判断还有没有当前专场其他待支付的订单）
                if order_object.deposit.balance > 0:
                    if order_object.deposit.deposit_type == 1:
                        # 单品保证金

                        # 退保证金记录
                        deposit_refund_object = models.DepositRefundRecord(
                            uid=str(uuid.uuid4()),
                            status=2,
                            deposit=order_object.deposit,
                            amount=order_object.deposit.balance
                        )
                        # 退款到原账户
                        request.user.balance = request.user.balance + order_object.deposit.balance

                    else:
                        # 全场保证金
                        exists = models.Order.objects.filter(
                            user=request.user,
                            status=1,
                            item__auction_id=order_object.deposit.auction_id).exclude(id=order_object.id).exists()
                        if not exists:
                            # 退保证金记录
                            deposit_refund_object = models.DepositRefundRecord(
                                uid=str(uuid.uuid4()),
                                status=2,
                                deposit=order_object.deposit,
                                amount=order_object.deposit.balance
                            )
                            # 退款到原账户
                            request.user.balance = request.user.balance + order_object.deposit.balance

            else:
                # 单品保证金
                if order_object.deposit.deposit_type == 1:
                    # 保证金余额
                    if order_object.deposit.balance > real_price:

                        # 抵扣 real_price
                        deposit_deduct_object = models.DepositDeduct(
                            order=order_object,
                            amount=real_price,
                            deduct_type=2
                        )
                        # 剩余的保证金退款处理（原途径）
                        """
                        if order_object.deposit.pay_type == 1:
                            # 微信退还
                        else:
                            # 余额退还
                        """
                        request.user.balance = request.user.balance + order_object.deposit.balance - real_price

                        # 退保证金记录
                        deposit_refund_object = models.DepositRefundRecord(
                            uid=str(uuid.uuid4()),
                            status=2,
                            deposit=order_object.deposit,
                            amount=order_object.deposit.balance - real_price
                        )

                        # 保证金的余额减为 0
                        order_object.deposit.balance = 0

                        # 之后 付款 0
                        real_price = 0
                    else:
                        # 保证金比较少
                        real_price = real_price - order_object.deposit.balance

                        # 保证金抵扣记录
                        deposit_deduct_object = models.DepositDeduct(
                            order=order_object,
                            amount=order_object.deposit.balance,
                            deduct_type=2
                        )

                        # 保证金余额为0
                        order_object.deposit.balance = 0

                # 专场保证金
                else:
                    if order_object.deposit.balance > real_price:
                        # 抵扣 real_price
                        deposit_deduct_object = models.DepositDeduct(
                            order=order_object,
                            amount=real_price,
                            deduct_type=2
                        )
                        # 判断当前用户在当前专场下是否还拍到其他未支付的订单
                        exists = models.Order.objects.filter(
                            user=request.user,
                            status=1,
                            item__auction_id=order_object.deposit.auction_id).exclude(id=order_object.id).exists()
                        if exists:
                            # 不退保证金 + 保证金余额应该处理（余额-real_price）
                            order_object.deposit.balance = order_object.deposit.balance - real_price
                        else:
                            # 退保证金到用户余额
                            request.user.balance = request.user.balance + (order_object.deposit.balance - real_price)

                            # 退保证金记录
                            deposit_refund_object = models.DepositRefundRecord(
                                uid=str(uuid.uuid4()),
                                status=2,
                                deposit=order_object.deposit,
                                amount=order_object.deposit.balance - real_price
                            )

                            # 保证金的余额减为 0
                            order_object.deposit.balance = 0

                        # 之后付款 0
                        real_price = 0
                    else:
                        # 保证金少 ,需要支付多

                        # 抵扣 real_price
                        deposit_deduct_object = models.DepositDeduct(
                            order=order_object,
                            amount=order_object.deposit.balance,
                            deduct_type=2
                        )

                        # 之后 付款
                        real_price = real_price - order_object.deposit.balance

                        # 保证金的余额减为 0
                        order_object.deposit.balance = 0

            # ## 2.4 应付金额判断
            if real_pay != real_price:
                raise exceptions.ValidationError('前端和后端支付价格不一致')

            # 3.支付
            """
            if pay_type == 1:
                # 微信支付
                #   与支付订单的ID，签名给小程序返回json数据
                #   小程序中进行支付
                #       用户支付，
                #       用不不支付
                #   将订单和各种抵扣全都处理，但订单状态 先变更为 未支付，支付中，->已支付 （回调函数）
                pass
            else:
                # 余额支付
                pass
            """

            if request.user.balance < real_price:
                raise exceptions.ValidationError('余额不够，请充值')

            # 通过余额去支付
            request.user.balance = request.user.balance - real_price

            # 4. 数据更新
            # 对订单进行修改(带收货 -> 完成 )
            models.Order.objects.filter(id=order_object.id).update(real_price=real_price, pay_type=2, status=3,
                                                                   address_id=address_id)
            # 抵扣记录
            if deposit_deduct_object:
                deposit_deduct_object.save()
            # 退款记录
            if deposit_refund_object:
                deposit_refund_object.save()
            # 如果用了优惠券
            if coupon_object:
                coupon_object.save()
            # 余额退还
            request.user.save()

            # 此订单关联用户保证金余额提交数据（余额清空）
            order_object.deposit.save()

        return Response({},status=status.HTTP_200_OK)


class AddressView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthentication, ]
    serializer_class = AddressModelSerializer

    def get_queryset(self):
        return models.Address.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
