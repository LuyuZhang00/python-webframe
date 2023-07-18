#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from utils.response import BaseResponse


def send_china_msg(phone, code):
    """
    发送短信
    :param code:短信验证码，如：86
    :param phone: 手机号，示例："15131255555"
    :return:
    """
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    response = BaseResponse()
    try:
        phone = "{}{}".format("+86", phone)
        cred = credential.Credential("AKIDW3Rgszw84ylQxMzNn7KOJ6kFPSL5c5MU", "GQSMXmtsjR0QhuIalzTp250nU6digZSD")
        client = sms_client.SmsClient(cred, "ap-guangzhou")

        req = models.SendSmsRequest()
        req.SmsSdkAppid = "1400302209"
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
        req.Sign = "Python之路"
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = [phone, ]
        # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
        req.TemplateID = "516680"
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [code, ]

        resp = client.SendSms(req)

        response.message = resp.SendStatusSet[0].Message
        if resp.SendStatusSet[0].Code == "Ok":
            response.status = True

    except TencentCloudSDKException as err:
        response.message = err.message

    return response


if __name__ == '__main__':
    result = send_china_msg("999", "15131255089")
    print(result.status, result.message)
