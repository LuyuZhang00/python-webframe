#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from rest_framework.exceptions import ValidationError


def phone_validator(value):
    """
    手机号格式验证
    :param value:
    :return:
    """
    regex = r'^(1[3|4|5|6|7|8|9])\d{9}$'
    if not re.match(regex, value):
        raise ValidationError('手机格式错误')


def message_code_validator(value):
    if not value.isdecimal() or len(value) != 4:
        raise ValidationError('短信验证码格式错误')
