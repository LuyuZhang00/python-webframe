#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from utils.tencent.msg import send_china_msg
from utils.tencent.oss import get_credential
from ..serializers.auth import MessageCodeSerializer, LoginSerializer
from .. import models

from utils.encrypt import create_uid


class MessageView(APIView):
    """
    短信验证码
    """

    def get(self, request, *args, **kwargs):
        """
        获取用户手机号并发送短信，如果超出范围则返回提示信息。
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1. 验证手机格式
        # 2. 创建验证码
        # 3. 发送短信
        # 4. 保存到redis（设置超时时间为1分钟）
        ser = MessageCodeSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({"status": False, "message": "验证码格式错误"})

        random_code = random.randrange(1000, 9999)
        phone = ser.validated_data.get('phone')

        result = send_china_msg(phone, random_code)
        if not result.status:
            return Response({"status": False, "message": "验证码发送失败"})

        conn = get_redis_connection()
        conn.set(phone, random_code, ex=30)

        return Response({"status": True, 'message': '验证码发送成功'})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        """ 用户登录接口 """

        # ########################## 线上正式操作 ##########################
        """ 
        # 1. 校验用户输入的合法性
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'detail': ser.errors, 'message': "验证码错误"})

        # 2. 获取微信session_key和openid
        #    https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html
        wx_code = ser.validated_data.pop('wx_code')
        params = {
            'appid': 'wx55cca0b94f723dc7',
            'secret': 'c000e3ddc95d2ef723b9b010f0ae05d5',
            'js_code': wx_code,
            'grant_type': 'authorization_code'

        }
        result_dict = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params).json()

        # 3.创建或更新账户
        phone = request.validated_data.pop('phone')
        token = create_uid(phone)
        user_object = models.UserInfo.objects.filter(telephone=phone).first()
        if not user_object:
            models.UserInfo.objects.create(**{**ser.validated_data, **result_dict}, token=token, telephone=phone)
        else:
            models.UserInfo.objects.filter(telephone=phone).update(**{**ser.validated_data, **result_dict}, token=token)

        # 4.给用户返回相应信息
        return Response({'status': True, 'data': {'token': token, 'phone': phone}})
        """

        # ########################## 临时操作 ##########################
        # 1. 获取微信session_key和openid
        #    https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html
        wx_code = request.data.get('wx_code')
        params = {
            'appid': 'wx55cca0b94f723dc7',
            'secret': 'c000e3ddc95d2ef723b9b010f0ae05d5',
            'js_code': wx_code,
            'grant_type': 'authorization_code'

        }
        result_dict = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params).json()

        # 2. 创建或更新账户
        phone = request.data.get('phone')
        token = create_uid(phone)
        user_object = models.UserInfo.objects.filter(telephone=phone).first()
        if not user_object:
            models.UserInfo.objects.create(
                **result_dict,
                token=token,
                telephone=phone,
                nickname=request.data.get('nickname'),
                avatar=request.data.get('avatar'),
            )
        else:
            models.UserInfo.objects.filter(telephone=phone).update(
                **result_dict,
                token=token,
                nickname=request.data.get('nickname'),
                avatar=request.data.get('avatar')
            )

        # 3.给用户返回相应信息
        return Response({'status': True, 'data': {'token': token, 'phone': phone}})


class OssCredentialView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(get_credential())
