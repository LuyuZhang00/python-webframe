#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from apps.api import models
from rest_framework import exceptions


class GeneralAuthentication(BaseAuthentication):
    """ 通用认证（所有页面都可以应用）

    如果用户已登录，则在request.user和request.auth中赋值；未登录则做任何操作。
    用户需要在请求头Authorization中传递token，格式如下：
        Authorization: token 401f7ac837da42b97f613d789819ff93537bee6a

    建议：配合和配置文件一起使用，未认证的用户request.user和request.auth的值为None

    REST_FRAMEWORK = {
        "UNAUTHENTICATED_USER":None,
        "UNAUTHENTICATED_TOKEN":None
    }

    """
    keyword = "token"

    def authenticate(self, request):
        auth_tuple = get_authorization_header(request).split()

        # 1.如果没有传token，则通过本次认证，进行之后的认证
        if not auth_tuple:
            return None

        # 2.如果传递token，格式不符，则通过本次认证，进行之后的认证
        if len(auth_tuple) != 2:
            return None

        # 3.如果传递了token，但token的名称不符，则通过本次认证，进行之后的认证
        if auth_tuple[0].lower() != self.keyword.lower().encode():
            return None

        # 4.对token进行认证，如果通过了则给request.user和request.auth赋值，否则返回None
        try:
            token = auth_tuple[1].decode()
            user_object = models.UserInfo.objects.get(token=token)
            return (user_object, token)
        except Exception as e:
            return None


class UserAuthentication(BaseAuthentication):
    keyword = "token"

    def authenticate(self, request):
        auth_tuple = get_authorization_header(request).split()

        if not auth_tuple:
            raise exceptions.AuthenticationFailed('认证失败')

        if len(auth_tuple) != 2:
            raise exceptions.AuthenticationFailed('认证失败')

        if auth_tuple[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed('认证失败')
        try:
            token = auth_tuple[1].decode()
            user_object = models.UserInfo.objects.get(token=token)
            return (user_object, token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('认证失败')
