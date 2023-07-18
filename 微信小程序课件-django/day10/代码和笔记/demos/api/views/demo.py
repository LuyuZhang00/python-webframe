import uuid
from django.shortcuts import render, HttpResponse
from api import models


def cos_upload(file_object, file_name):
    # 1.将文件写到本地
    # with open('xxx.png',mode='wb') as f:
    #     for line in cover:
    #         f.write(line)
    # 2.基于Python将文件对象保存到腾讯云COS
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client

    secret_id = 'AKIDW3Rgszw84ylQxMzNn7KOJ6kFPSL5c5MU'  # 替换为用户的 secretId
    secret_key = 'GQSMXmtsjR0QhuIalzTp250nU6digZSD'  # 替换为用户的 secretKey
    region = 'ap-chengdu'  # 替换为用户的 Region
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    client = CosS3Client(config)
    response = client.upload_file_from_buffer(
        Bucket='auction-1251317460',
        Body=file_object,
        Key=file_name
    )
    return "https://{0}.cos.{1}.myqcloud.com/{2}".format('auction-1251317460', region, file_name)


def demo(request):
    if request.method == "GET":
        return render(request, 'demo.html')
    title = request.POST.get('title')  # 字符串
    cover = request.FILES.get('cover')  # 文件对象
    ext = cover.name.rsplit('.', maxsplit=1)[-1]
    file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
    cos_path = cos_upload(cover, file_name)
    models.Auction.objects.create(title=title, cover=cos_path)
    return HttpResponse('...')
