from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from app01 import models
import uuid
import random
import requests
from rest_framework.generics import ListAPIView
from rest_framework import serializers
import time
from xml.etree import ElementTree as ET
class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        phone = request.data.get('phone')
        wx_code = request.data.get('wx_code')
        # openid的获取：需要拿着wx_code去微信申请
        #  https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html
        info = {
            'appid':"wx55cca0b94f723dc7", # 微信小程序
            'secret':"c000e3ddc95d2ef723b9b010f0ae05d5", # 微信小程序
            'js_code':wx_code,
            'grant_type':"authorization_code",
        }
        result = requests.get(url='https://api.weixin.qq.com/sns/jscode2session',params=info)
        openid = result.json()['openid']
        exists = models.UserInfo.objects.filter(phone=phone).exists()
        token = str(uuid.uuid4())
        if not exists:
            models.UserInfo.objects.create(
                phone=phone,
                token=token,
                openid = openid
            )
        else:
            models.UserInfo.objects.filter(phone=phone).update(token=token,openid=openid)

        return Response({'token':token})

def md5(string):
    import hashlib
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = "__all__"

class GoodsView(ListAPIView):
    queryset = models.Goods.objects
    serializer_class = GoodsModelSerializer


class PaymentView(APIView):

    def post(self,request,*args,**kwargs):
        goods_id = request.data.get('goodsId')
        order_random_string = str(int(time.time()))
        user_object = models.UserInfo.objects.filter(id=1).first() # user_object.openid
        goods_object = models.Goods.objects.filter(id=goods_id).first() # goods_object.price
        order_object = models.Order.objects.create(goods=goods_object,user=user_object,uid=order_random_string,status=1)

        # 按照微信的规则，去生成支付需要的一大堆的数据
        # https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=7_3&index=1
        print(order_random_string)
        # ###################### 1.调用支付统一下单 ######################
        info = {
            'appid': 'wx55cca0b94f723dc7',
            'mch_id': '1526049051',
            'device_info': 'wupeiqi-min-program',
            'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),
            'sign_type': "MD5",
            'body': "保证金",
            'detail': '这是一个商品详细描述信息.',
            'attach': '微信小程序',
            'out_trade_no': order_random_string,
            'total_fee': goods_object.price,  # 总金额
            'spbill_create_ip': request.META.get('REMOTE_ADDR'),  # 终端IP（用户IP） remote_addr = request.META.get('REMOTE_ADDR')
            'notify_url': "http://47.93.4.198:8012/pay/notify/",  # 支付成功之后，微信异步通知
            'trade_type': 'JSAPI',
            'openid': user_object.openid  # openid
        }
        # 1.1 签名
        #       对字典中的key按照ASCII码从小到大排序
        #       将排完序的值拼接 stringA = appid=wx55cca0b94f723dc7&mch_id=1526049051
        #       让stringA和key拼接：stringSignTemp = stringA+"&key=192006250b4c09247ec02edce69f6a2d" key为商户平台设置的密钥key
        #       MD5(stringSignTemp)
        #       将密文转换为大写
        #       得到签名 sign
        #       把签名再添加到info中    info['sign'] = sign值
        pay_key = "2SzCvaKgYExuItWBfYAqJFs72uUleD14"
        temp = "&".join(["{0}={1}".format(k, info[k]) for k in sorted(info)] + ["{0}={1}".format("key", pay_key, ), ])
        sign = md5(temp).upper()
        info['sign'] = sign
        # 1.2 向 https://api.mch.weixin.qq.com/pay/unifiedorder 发请求 (json转换为xml)

        xml_string = "<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in info.items()]))
        prepay = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data=xml_string.encode('utf-8'))
        # 1.3 从结果xml中提取 prepay_id

        root = ET.XML(prepay.content.decode('utf-8'))
        prepay_dict = {child.tag:child.text for child in root}
        prepay_id = prepay_dict['prepay_id']

        # ####################### 2.再次签名 #######################
        info_dict = {
            'appId': "wx55cca0b94f723dc7",
            'timeStamp': str(int(time.time())),  # 时间戳从1970年1月1日00:00:00至今的秒数,即当前的时间
            'nonceStr': "".join([chr(random.randint(65, 90)) for _ in range(12)]),  # 随机字符串，长度为32个字符以下。
            'package': 'prepay_id={0}'.format(prepay_id),  # 统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=*
            'signType': 'MD5',  # 签名类型，默认为MD5，支持HMAC-SHA256和MD5。注意此处需与统一下单的签名类型一致
        }
        temp = "&".join(
            ["{0}={1}".format(k, info_dict[k]) for k in sorted(info_dict)] + ["{0}={1}".format("key", pay_key, ), ])
        sign2 = md5(temp).upper()
        info_dict['paySign'] = sign2

        return Response(info_dict)






class NotifyView(APIView):
    """
    支付完成之后的通知
    """

    def post(self,request,*args,**kwargs):
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
            models.Order.objects.filter(uid=out_trade_no).update(status=2)
            response = """<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"""
            return Response(response)























