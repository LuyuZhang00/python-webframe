import re
import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from api import models
from utils.tencent.msg import send_message
from api.serializer.account import MessageSerializer, LoginSerializer


class MessageView(APIView):
    """
    发送短信接口
    """

    def get(self, request, *args, **kwargs):
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'message': '手机格式错误'})
        phone = ser.validated_data.get('phone')
        random_code = random.randint(1000, 9999)
        """
        result = send_message(phone,random_code)
        if not result:
            return Response({"status": False, 'message': '短信发送失败'})
        """
        print(random_code)
        """
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=60)
        """
        return Response({"status": True, 'message': '发送成功'})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        """"""

        # 正式操作
        """
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '验证码错误'})

        phone = ser.validated_data.get('phone')
        nickname = ser.validated_data.get('nickname')
        avatar = ser.validated_data.get('avatar')
        """
        # 临时操作
        phone = request.data.get('phone')
        nickname = request.data.get('nickname')
        avatar = request.data.get('avatar')

        user_object, flag = models.UserInfo.objects.get_or_create(
            telephone=phone,
            defaults={
                "nickname": nickname,
                'avatar': avatar}
        )
        user_object.token = str(uuid.uuid4())
        user_object.save()

        return Response({"status": True, "data": {"token": user_object.token, 'phone': phone}})
