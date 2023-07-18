#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
import requests
from xml.etree import ElementTree as ET

from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from utils.filters import BidItemFilter
from utils.encrypt import create_uid, md5
from utils.auth import UserAuthentication
from utils.permissions import BidPermission
from utils.pagination import RollLimitOffsetPagination
from utils.filters import ReachBottomFilter, PullDownRefreshFilter

from apps.api import models
from apps.api.serializers.bid import BidModelSerializer
from apps.api.serializers.deposit import AuctionDepositModelSerializer, PayDepositSerializer
from apps.api.serializers.auction import AuctionModelSerializer, AuctionDetailModelSerializer


class AuctionView(ListAPIView):
    """ 专场列表接口 """
    queryset = models.Auction.objects.exclude(status=1).order_by('-id')
    serializer_class = AuctionModelSerializer
    filter_backends = [ReachBottomFilter, PullDownRefreshFilter]
    pagination_class = RollLimitOffsetPagination


class AuctionDetailView(RetrieveAPIView):
    """ 专场详细（拍品列表）接口 """
    queryset = models.Auction.objects.exclude(status=1)
    serializer_class = AuctionDetailModelSerializer


class AuctionDepositView(RetrieveAPIView):
    """ 保证金页面展示 """
    authentication_classes = [UserAuthentication, ]

    serializer_class = AuctionDepositModelSerializer
    queryset = models.AuctionItem.objects.select_related('auction').filter(auction__status=3)


class PayDepositView(APIView):
    """ 保证金支付 """
    authentication_classes = [UserAuthentication, ]

    def post(self, request, *args, **kwargs):
        ser = PayDepositSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        item_id = ser.validated_data.pop('item_id')
        pay_type = ser.validated_data['pay_type']
        deposit_type = ser.validated_data['deposit_type']
        amount = ser.validated_data['amount']

        uid = create_uid(request.user.nickname)
        # 1. 余额支付
        if pay_type == 2:
            with transaction.atomic():
                request.user.balance -= - amount
                request.user.save()
                models.DepositRecord.objects.create(**ser.validated_data, status=2, uid=uid, user=request.user,
                                                    item_id=item_id if deposit_type == 1 else None,
                                                    balance=amount
                                                    )
            return Response({'msg': '余额支付成功'}, status=status.HTTP_200_OK)
        # 2. 微信支付
        if pay_type == 1:
            # 创建时，状态应该是1，在回调再次确认时，状态应为2.
            models.DepositRecord.objects.create(**ser.validated_data, status=2, uid=uid, user=request.user,
                                                item_id=item_id if deposit_type == 1 else None,
                                                balance=amount
                                                )
            # ########### 2.1 创建预支付交易单 ###########
            #   https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_7
            #   https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=7_4&index=3

            # 商户支付的key，去自己的商户平台获取
            pay_key = "2SzCvaKgYExuItWBfYAqJFs72uUleD14"

            data = {
                'appid': 'wx55cca0b94f723dc7',
                'mch_id': '1526049051',
                'device_info': 'wupeiqi-min-program',
                'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),
                'sign_type': "MD5",
                'body': "保证金",
                'detail': '这是一个商品详细描述信息.',
                'attach': '微信小程序',
                'out_trade_no': uid,  # 商户系统内部订单号
                'total_fee': 1,  # 总金额
                'spbill_create_ip': '1.1.1.1',  # 终端IP（用户IP）
                'notify_url': "http://47.93.4.198:8012/pay/notify/",  # 支付成功之后，微信异步通知
                'trade_type': 'JSAPI',
                'openid': request.user.openid  # openid
            }

            temp = "&".join(
                ["{0}={1}".format(k, data[k]) for k in sorted(data)] + ["{0}={1}".format("key", pay_key, ), ])
            pre_sign = md5(temp).upper()
            data['sign'] = pre_sign

            xml_string = "<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in data.items()]))
            prepay = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml_string.encode('utf-8'))
            root = ET.XML(prepay.content.decode('utf-8'))
            prepay_result = {child.tag: child.text for child in root}

            prepay_id = prepay_result['prepay_id']

            # ########### 2.2 创建支付签名 ###########
            random_string = "".join([chr(random.randint(65, 90)) for _ in range(12)])
            info = {
                'appId': "wx55cca0b94f723dc7",
                'timeStamp': str(int(time.time())),  # 时间戳从1970年1月1日00:00:00至今的秒数,即当前的时间
                'nonceStr': random_string,  # 随机字符串，长度为32个字符以下。
                'package': 'prepay_id={0}'.format(prepay_id),  # 统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=*
                'signType': 'MD5',  # 签名类型，默认为MD5，支持HMAC-SHA256和MD5。注意此处需与统一下单的签名类型一致
            }
            temp = "&".join(
                ["{0}={1}".format(k, info[k]) for k in sorted(info)] + ["{0}={1}".format("key", pay_key, ), ])
            sign = md5(temp).upper()
            info['paySign'] = sign

            return Response(info, status=status.HTTP_200_OK)


class PayDepositNotifyView(APIView):
    """
    保证金支付成功后进行通知
    """

    def post(self, request, *args, **kwargs):
        # 1. 获取结果把结果XML转换为字典格式
        root = ET.XML(request.body.decode('utf-8'))
        result = {child.tag: child.text for child in root}

        # 2. 校验签名是否正确，防止恶意请求。
        sign = result.pop('sign')

        # key为商户平台设置的密钥key
        key = "2SzCvaKgYExuItWBfYAqJFs72uUleD14"
        temp = "&".join(
            ["{0}={1}".format(k, result[k]) for k in sorted(result)] + ["{0}={1}".format("key", key, ), ])
        local_sign = md5(temp).upper()

        # 签名一致
        if local_sign == sign:
            # 根据订单号，把数据库的订单状态修改为支付成功
            out_trade_no = result.get('out_trade_no')
            models.DepositRecord.objects.filter(uid=out_trade_no).update(status=2)  # 支付成功
            response = """<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"""
            return Response(response)


class BidView(ListAPIView, CreateAPIView):
    """
    展示出价记录接口 & 出价
    """
    authentication_classes = [UserAuthentication, ]
    permission_classes = [BidPermission, ]
    queryset = models.BidRecord.objects.all().order_by('-id')
    serializer_class = BidModelSerializer
    filter_backends = [BidItemFilter, ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return response
        item_id = request.query_params.get('item_id')
        item_object = models.AuctionItem.objects.filter(id=item_id).first()

        context = {
            'unit': item_object.unit,
            'price': response.data[0]['price'] if response.data else item_object.start_price,
            'bid_list': response.data
        }
        response.data = context
        return response

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, status=1)
