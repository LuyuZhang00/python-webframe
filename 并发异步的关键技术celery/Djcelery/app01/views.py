from django.shortcuts import render,HttpResponse

# Create your views here.
from mycelery.sms.tasks import send_sms,send_sms2


def test(request):

    # 异步任务
    # 1. 声明一个和celery一模一样的任务函数，但是我们可以导包来解决

    send_sms.delay("110")
    send_sms2.delay("119")
    # send_sms.delay() 如果调用的任务函数没有参数，则不需要填写任何内容

    # 定时任务







    return HttpResponse("OK")