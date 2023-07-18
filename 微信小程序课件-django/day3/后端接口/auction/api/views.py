from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import re

def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$",value):
        raise ValidationError('手机格式错误')

class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号',validators=[phone_validator,])

class MessageView(APIView):
    def get(self,request,*args,**kwargs):
        """
        发送手机短信验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status':False,'message':'手机格式错误'})
        phone = ser.validated_data.get('phone')
        # 3.生成随机验证码
        import random
        random_code = random.randint(1000,9999)

        # 4.验证码发送到手机上，购买服务器进行发送短信：腾讯云
        # TODO tencent.send_message(phone,random_code)
        """
            1.注册腾讯云，开通腾讯云短信。
            2.创建应用
                SDK AppID = 1400302209
            3.申请签名（个人：公众号）
                ID      名称
                260514	 Python之路
            4.申请模板
                ID      名称
                516680	miniprogram
            5.申请腾讯云API https://console.cloud.tencent.com/cam/capi
                SecretId:
                SecretKey:
            6.调用相关接口去发送短信 https://cloud.tencent.com/document/product/382/38778
                SDK，写好的工具。
                
        """
        from tencentcloud.common import credential
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.sms.v20190711 import sms_client, models
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        try:

            cred = credential.Credential("secretId", "secretKey")
            client = sms_client.SmsClient(cred, "ap-guangzhou")
            req = models.SendSmsRequest()

            # 短信应用ID: 短信SdkAppid在 [短信控制台] 添加应用后生成的实际SdkAppid，示例如1400006666
            req.SmsSdkAppid = "1400787878"
            # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
            req.Sign = "xxx"
            # 下发手机号码，采用 e.164 标准，+[国家或地区码][手机号]
            # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
            req.PhoneNumberSet = ["+8613711112222"]
            # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
            req.TemplateID = "449739"
            # 模板参数: 若无模板参数，则设置为空
            req.TemplateParamSet = ["666"]

            # 通过client对象调用DescribeInstances方法发起请求。注意请求方法名与请求对象是对应的。
            # 返回的resp是一个DescribeInstancesResponse类的实例，与请求对象对应。
            resp = client.SendSms(req)

            # 输出json格式的字符串回包
            print(resp.to_json_string(indent=2))

        except TencentCloudSDKException as err:
            print(err)


        # 5.把验证码+手机号保留（30s过期）
        """
        #   5.1 搭建redis服务器（云redis）
        #   5.2 django中方便使用redis的模块 django-redis
               配置:
                    CACHES = {
                        "default": {
                            "BACKEND": "django_redis.cache.RedisCache",
                            "LOCATION": "redis://127.0.0.1:6379",
                            "OPTIONS": {
                                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                                "CONNECTION_POOL_KWARGS": {"max_connections": 100}
                                # "PASSWORD": "密码",
                            }
                        }
                    }
                使用：
        """
        from django_redis import get_redis_connection
        conn = get_redis_connection()
        conn.set(phone,random_code,ex=30)

        return Response({"status": True,'message':'发送成功'})


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        print(request.data)
        return Response({"status":True})

