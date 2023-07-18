#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
import json
import time
import random
import hashlib
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.tencent.msg import send_china_msg
from ..serializers.auth import MessageCodeSerializer, LoginSerializer
from .. import models
from django_redis import get_redis_connection


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
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        """
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'detail': ser.errors,'message':"验证码错误"})
        # 2. 获取或创建用户
        phone = ser.validated_data.get('phone')
        """
        phone = request.data.get('phone')
        user_object, flag = models.UserInfo.objects.get_or_create(telephone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()

        """
        # 获取微信 session_key 和 openid
        params = {
            'appid': 'wx55cca0b94f723dc7',
            'secret': 'c000e3ddc95d2ef723b9b010f0ae05d5',
            'js_code': request.data.get('code'),
            'grant_type': 'authorization_code'

        }
        res = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params).json()
        # {'session_key': '8m1jCCqA2x+enLdoEmFAXg==', 'openid': 'ofuZp5MaP33ezAlO8gcsgEY_jpac'}
        """

        return Response({'status': True, 'data': {'token': user_object.token, 'phone': phone}})


class OssCredentialView(APIView):

    def get(self, request, *args, **kwargs):
        from utils.tencent.oss import get_credential

        return Response(get_credential())
