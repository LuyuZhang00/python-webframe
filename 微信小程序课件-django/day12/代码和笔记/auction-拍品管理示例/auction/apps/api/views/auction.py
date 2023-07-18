#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from django.db import transaction
from utils.auth import UserAuthentication, GeneralAuthentication
from xml.etree import ElementTree as ET

from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework import exceptions

from apps.api import models
from utils.filters import ReachBottomFilter, PullDownRefreshFilter
from utils.pagination import RollLimitOffsetPagination
from utils.encrypt import create_uid, md5


# ############################## 拍卖列表 ##############################

class AuctionModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = ['id', 'title', 'status', 'cover', 'total_price', 'look_count', 'goods_count', 'items']

    def get_status(self, obj):
        status_class_mapping = {
            2: 'preview',
            3: 'auction',
            4: 'stop'
        }
        return {'text': obj.get_status_display(), 'class': status_class_mapping.get(obj.status)}

    def get_items(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj)[0:5]
        return [row.cover for row in queryset]


class AuctionView(ListAPIView):
    queryset = models.Auction.objects.exclude(status=1).order_by('-id')
    serializer_class = AuctionModelSerializer
    filter_backends = [ReachBottomFilter, PullDownRefreshFilter]
    pagination_class = RollLimitOffsetPagination


# ############################## 拍卖详细 ##############################

class AuctionDetailItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuctionItem
        fields = [
            'id', 'status', 'cover', 'unit', 'title', 'start_price',
            'deal_price', 'reserve_price', 'highest_price'
        ]


class AuctionDetailModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    deposit = serializers.SerializerMethodField(label='保证金')

    class Meta:
        model = models.Auction
        fields = ['id', 'status', 'title', 'cover', 'look_count', 'goods_count', 'bid_count', 'items', 'deposit']

    def get_status(self, obj):
        status_class_mapping = {
            2: 'preview',
            3: 'auction',
            4: 'stop'
        }
        return {'text': obj.get_status_display(), 'class': status_class_mapping.get(obj.status)}

    def get_items(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj).exclude(status=1)
        ser = AuctionDetailItemModelSerializer(instance=queryset, many=True)
        return ser.data

    def get_deposit(self, obj):
        context = {
            'total': False,
            'single': {}
        }
        user_object = self.context['request'].user
        if not user_object:
            return context
        queryset = models.DepositRecord.objects.filter(user=user_object, auction=obj, status=2)
        if not queryset.exists():
            return context

        if queryset.filter(deposit_type=2).exists():
            context['total'] = True
            return context

        context['single'] = {row.item_id: True for row in queryset}
        return context


class AuctionDetailView(RetrieveAPIView):
    queryset = models.Auction.objects.exclude(status=1)
    serializer_class = AuctionDetailModelSerializer


# ###################### 3. 保证金  ######################

class AuctionDepositModelSerializer(serializers.ModelSerializer):
    deposit = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

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


class AuctionDepositView(RetrieveAPIView):
    authentication_classes = [UserAuthentication, ]

    serializer_class = AuctionDepositModelSerializer
    queryset = models.AuctionItem.objects.select_related('auction').filter(auction__status=3)


# ###################### 4. 保证金支付  ######################

class PayDepositSerializer(serializers.Serializer):
    auction_id = serializers.IntegerField(label='拍卖ID')
    item_id = serializers.IntegerField(label='拍品ID')
    deposit_type = serializers.IntegerField(label='保证金类型')
    amount = serializers.IntegerField(label='付款金额')
    pay_type = serializers.IntegerField(label='支付方式')

    def validate_auction_id(self, value):
        """ 检查是否已支付全场保证金 """
        user_object = self.context['request'].user
        exists = models.DepositRecord.objects.filter(user=user_object, auction_id=value, item__isnull=True).exists()
        if exists:
            raise exceptions.ValidationError(detail='已支付过全场保证金')
        return value

    def validate_item_id(self, value):
        """ 检查是否已支付单品保证金 """
        user_object = self.context['request'].user
        exists = models.DepositRecord.objects.filter(user=user_object, item__id=value).exists()
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
            exists = models.DepositRecord.objects.filter(user=user_object, auction_id=auction_id).exists()
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


class PayDepositView(APIView):
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
                                                    )
            return Response({'msg': '余额支付成功'}, status=status.HTTP_200_OK)
        # 2. 微信支付
        if pay_type == 1:
            # 创建时，状态应该是1，在回调再次确认时，状态应为2.
            models.DepositRecord.objects.create(**ser.validated_data, status=2, uid=uid, user=request.user,
                                                item_id=item_id if deposit_type == 1 else None,
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


# ###################### 4. 保证金支付  ######################
class PayDepositNotifyView(APIView):
    """
    保证金 微信支付成功 之后异步通知
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


# ##################### 5.出价 ##########################
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import BasePermission


class BidItemFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        item_id = request.query_params.get('item_id')
        if not item_id:
            return queryset.none
        return queryset.filter(item_id=item_id)


class BidPermission(BasePermission):
    def has_permission(self, request, view):
        """
        校验是否具有权限，当前用户如果未付保证金，则无权访问
        """

        item_id = request.query_params.get('item_id')
        exists = models.DepositRecord.objects.filter(user=request.user,
                                                     item_id=item_id,
                                                     status=2,
                                                     item__status=1).exists()
        return exists

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class BidModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.nickname', read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = models.BidRecord
        exclude = ['user', 'status', ]

    def validate_item(self, value):
        """ 验证是否还正在拍卖"""
        item_id = self.initial_data.get('item')
        exists = models.AuctionItem.objects.filter(id=item_id, status=1).exists()
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


class BidView(ListAPIView, CreateAPIView):
    """
    出价记录
    """
    authentication_classes = [UserAuthentication, ]
    permission_classes = [BidPermission, ]
    queryset = models.BidRecord.objects.all().order_by('-id')
    serializer_class = BidModelSerializer

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
