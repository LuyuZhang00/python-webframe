from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models

from django.conf import settings

def send_message(phone,random_code,template_id="516680"):
    """
    发送短信验证码
        验证码发送到手机上，购买服务器进行发送短信：腾讯云
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
    try:
        phone = "{}{}".format("+86", phone)
        cred = credential.Credential(settings.TENCENT_SECRET_ID, settings.TENCENT_SECRET_KEY)
        client = sms_client.SmsClient(cred, settings.TENCENT_CITY)

        req = models.SendSmsRequest()
        req.SmsSdkAppid = settings.TENCENT_APP_ID
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
        req.Sign = settings.TENCENT_SIGN
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = [phone, ]
        # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
        req.TemplateID = template_id
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [random_code, ]

        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        if resp.SendStatusSet[0].Code == "Ok":
            return True

    except TencentCloudSDKException as err:
        pass