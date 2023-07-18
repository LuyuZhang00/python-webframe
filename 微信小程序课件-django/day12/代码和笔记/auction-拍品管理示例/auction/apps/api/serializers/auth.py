#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .validators import phone_validator, message_code_validator

from django_redis import get_redis_connection

from .. import models


class MessageCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    code = serializers.CharField(label="验证码", validators=[message_code_validator, ])
    wx_code = serializers.CharField(label='微信临时登录凭证')
    nickname = serializers.CharField(label='微信昵称')
    avatar = serializers.CharField(label='微信头像')

    def validate_code(self, value):
        phone = self.initial_data.get('phone')
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError('短信验证码已失效')
        if value != code.decode('utf-8'):
            raise ValidationError('短信验证码错误')
        return value
