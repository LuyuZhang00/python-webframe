#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import random
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response


class PayView(APIView):

    def get(self, request, *args, **kwargs):
        def md5(string):
            ha = hashlib.md5()
            ha.update(string.encode('utf-8'))
            return ha.hexdigest()

        # 下单，生成预支付交易单
        # https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=9_1
        import requests

        data = {
            'appid': 'wx55cca7',
            'mch_id': '1526049051',
            'device_info': 'wupeiqi-min-program',
            'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),
            'sign_type': "MD5",
            'body': "拍卖-保证金",
            'detail': '这是一个商品详细描述信息.',
            'attach': '微信小程序',
            'out_trade_no': 'kkuisdf3sf123',  # 商户系统内部订单号
            'total_fee': 1,
            'spbill_create_ip': '1.1.1.1',
            'notify_url': "http://www.weixin.qq.com/wxpay/pay.php",
            'trade_type': 'JSAPI',
            'openid': "ofuZp5MaP33ezsgEY_jpac" # openid
        }
        pay_key = "2SzCvaKgYExuItWBUleD14"
        temp = "&".join(["{0}={1}".format(k, data[k]) for k in sorted(data)] + ["{0}={1}".format("key", pay_key, ), ])
        pre_sign = md5(temp).upper()
        data['sign'] = pre_sign

        xml_string = "<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in data.items()]))
        prepay = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml_string.encode('utf-8'))

        from xml.etree import ElementTree as ET
        root = ET.XML(prepay.content.decode('utf-8'))

        prepay_result = {}
        for child in root:
            # 第二层节点的标签名称和标签属性
            print(child.tag, child.text)
            prepay_result[child.tag] = child.text
        print(prepay_result)

        prepay_id = prepay_result['prepay_id']


        random_string = "".join([chr(random.randint(65, 90)) for _ in range(12)])
        info = {
            'appId': "wx55cca0bdc7",
            'timeStamp': str(int(time.time())),  # 时间戳从1970年1月1日00:00:00至今的秒数,即当前的时间
            'nonceStr': random_string,  # 随机字符串，长度为32个字符以下。
            'package': 'prepay_id={0}'.format(prepay_id),  # 统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=*
            'signType': 'MD5',  # 签名类型，默认为MD5，支持HMAC-SHA256和MD5。注意此处需与统一下单的签名类型一致
        }

        pay_key = "2SzCvaKgYYAqJFs72uUleD14"
        temp = "&".join(["{0}={1}".format(k, info[k]) for k in sorted(info)] + ["{0}={1}".format("key", pay_key, ), ])
        sign = md5(temp).upper()
        info['paySign'] = sign

        return Response(info)
