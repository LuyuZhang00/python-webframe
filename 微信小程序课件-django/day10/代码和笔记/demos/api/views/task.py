from django.shortcuts import HttpResponse
from api.tasks import x1
import datetime

def create_task(request):
    print('请求来了')
    # 1.立即执行
    # result = x1.delay(2,2)

    # 2.定时执行
    # 获取本地时间
    ctime = datetime.datetime.now()
    # 本地时间转换成utc时间
    utc_ctime = datetime.datetime.utcfromtimestamp(ctime.timestamp())
    target_time = utc_ctime + datetime.timedelta(seconds=10)
    result = x1.apply_async(args=[11, 3], eta=target_time)

    print('执行完毕')
    return HttpResponse(result.id)


def get_result(request):
    nid = request.GET.get('nid')
    from celery.result import AsyncResult
    # from demos.celery import app
    from demos import celery_app
    result_object = AsyncResult(id=nid, app=celery_app)

    # print(result_object.status) # 获取状态
    # data = result_object.get() # 获取数据
    # result_object.forget()  # 把数据在backend中移除。

    # # 取消任务
    # result_object.revoke()
    if result_object.successful():
        result_object.get()
        result_object.forget()
    elif result_object.failed():
        pass
    else:
        pass

    return HttpResponse('...')