#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import uuid
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.db.models import F
from apps.api import models
from apps.web.forms.auction import AuctionModelForm, AuctionItemAddModelForm, AuctionItemEditModelForm, \
    AuctionDetailModelForm, AuctionItemImageModelForm, CouponModelForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from utils.tencent.cos import upload_file

from apps.web import tasks
from auction import celery_app
from celery.result import AsyncResult


def auction_list(request):
    """
    拍卖系列列表
    :param request:
    :return:
    """
    queryset = models.Auction.objects.all().order_by('-id')
    return render(request, 'web/auction_list.html', {'queryset': queryset})


def auction_add(request):
    """
    创建拍卖任务
    :param request:
    :return:
    """
    if request.method == 'GET':
        ctime = datetime.datetime.now()
        form = AuctionModelForm(
            initial={
                'preview_start_time': ctime + datetime.timedelta(minutes=2),
                'preview_end_time': ctime + datetime.timedelta(minutes=3),
                'auction_start_time': ctime + datetime.timedelta(minutes=3),
                'auction_end_time': ctime + datetime.timedelta(minutes=10),
            }
        )
        return render(request, 'web/auction_form.html', {'form': form})
    form = AuctionModelForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        instance = form.save()

        # 1.定时任务，从 未开拍  预展
        preview_utc_datetime = datetime.datetime.utcfromtimestamp(form.instance.preview_start_time.timestamp())
        preview_task_id = tasks.to_preview_status_task.apply_async(args=[instance.id], eta=preview_utc_datetime).id

        # 2.定时任务，从 预展 到 开拍
        auction_utc_datetime = datetime.datetime.utcfromtimestamp(form.instance.auction_start_time.timestamp())
        auction_task_id = tasks.to_auction_status_task.apply_async(args=[instance.id], eta=auction_utc_datetime).id

        # 3.定时任务，从 开拍 到 拍卖结束
        auction_end_utc_datetime = datetime.datetime.utcfromtimestamp(form.instance.auction_end_time.timestamp())
        auction_end_task_id = tasks.end_auction_task.apply_async(args=[instance.id], eta=auction_end_utc_datetime).id

        models.AuctionTask.objects.create(
            preview_task=preview_task_id,
            auction_task=auction_task_id,
            auction_end_task=auction_end_task_id,
            auction=instance
        )

        return redirect('auction_list')
    return render(request, 'web/auction_form.html', {'form': form})


def auction_delete(request, pk):
    models.Auction.objects.filter(id=pk).delete()
    # 1.取消所有定时任务，根据ID来进行取消
    return JsonResponse({'status': True})


def auction_edit(request, pk):
    auction_object = models.Auction.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = AuctionModelForm(instance=auction_object)
        return render(request, 'web/auction_form.html', {'form': form})
    form = AuctionModelForm(data=request.POST, files=request.FILES, instance=auction_object)
    if form.is_valid():
        # 修改定时任务：如果时间不一致，则修改定时任务执行时间
        # 1.时间如果时间有变更 form.changed_data
        value = form.changed_data
        form.save()
        return redirect('auction_list')
    return render(request, 'web/auction_form.html', {'form': form})


def auction_item_list(request, auction_id):
    auction_object = models.Auction.objects.filter(id=auction_id).first()
    item_list = models.AuctionItem.objects.filter(auction=auction_object)
    context = {
        'auction_object': auction_object,
        'item_list': item_list
    }
    return render(request, 'web/auction_item_list.html', context)


@csrf_exempt
def auction_item_add(request, auction_id):
    auction_object = models.Auction.objects.filter(id=auction_id).first()
    if request.method == 'GET':
        form = AuctionItemAddModelForm()
        context = {
            'form': form,
            'auction_object': auction_object
        }
        return render(request, 'web/auction_item_add.html', context)

    form = AuctionItemAddModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.instance.auction = auction_object
        form.instance.uid = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        instance = form.save()

        models.Auction.objects.filter(id=auction_id).update(goods_count=F('goods_count') + 1)

        return JsonResponse({
            'status': True,
            'data': {
                'detail_url': reverse('auction_item_detail_add', kwargs={'item_id': instance.id}),
                'image_url': reverse('auction_item_image_add', kwargs={'item_id': instance.id}),
                'list_url': reverse('auction_item_list', kwargs={'auction_id': auction_id})
            }
        })

    return JsonResponse({'status': False, 'errors': form.errors})


def auction_item_edit(request, auction_id, item_id):
    item_object = models.AuctionItem.objects.filter(id=item_id).first()
    detail_object_list = models.AuctionItemDetail.objects.filter(item=item_object)
    image_object_list = models.AuctionItemImage.objects.filter(item=item_object)
    context = {
        "item_object": item_object,
        "detail_object_list": detail_object_list,
        "image_object_list": image_object_list
    }

    if request.method == 'GET':
        form = AuctionItemAddModelForm(instance=item_object)
    else:
        form = AuctionItemAddModelForm(instance=item_object, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    context['form'] = form
    return render(request, 'web/auction_item_edit.html', context)


def auction_item_delete(request, item_id):
    item_object = models.AuctionItem.objects.filter(id=item_id).first()
    if not item_object:
        return JsonResponse({'status': False, 'error': '拍品不存在'})

    models.Auction.objects.filter(id=item_object.auction_id).update(goods_count=F('goods_count') - 1)
    models.AuctionItem.objects.filter(id=item_id).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_detail_add(request, item_id):
    """
    创建规格
    :param request:
    :return:
    """
    detail_list = json.loads(request.body.decode('utf-8'))
    object_list = [models.AuctionItemDetail(**info, item_id=item_id) for info in detail_list if all(info.values())]
    models.AuctionItemDetail.objects.bulk_create(object_list)
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_detail_add_one(request, item_id):
    """
    添加规则
    :param request:
    :param item_id:
    :return:
    """
    if request.method != 'POST':
        return JsonResponse({'status': False})
    form = AuctionDetailModelForm(data=request.POST)
    if form.is_valid():
        form.instance.item_id = item_id
        instance = form.save()
        return JsonResponse({'status': True, 'data': {'id': instance.id}})
    return JsonResponse({'status': False, 'errors': form.errors})


@csrf_exempt
def auction_item_detail_delete_one(request):
    detail_id = request.GET.get('detail_id')
    models.AuctionItemDetail.objects.filter(id=detail_id).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_image_add(request, item_id):
    """
    创建图片
    :param request:
    :param item_id:
    :return:
    """
    show_list = request.POST.getlist('show')
    image_object_list = request.FILES.getlist('img')
    orm_object_list = []
    for index in range(len(image_object_list)):
        image_object = image_object_list[index]
        if not image_object:
            continue
        ext = image_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cos_path = upload_file(image_object, file_name)
        orm_object_list.append(models.AuctionItemImage(img=cos_path, item_id=item_id, carousel=bool(show_list[index])))
    if orm_object_list:
        models.AuctionItemImage.objects.bulk_create(orm_object_list)
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_image_add_one(request, item_id):
    form = AuctionItemImageModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.instance.item_id = item_id
        instance = form.save()
        return JsonResponse({'status': True, 'data': {'id': instance.id}})
    return JsonResponse({'status': False, 'errors': form.errors})


def auction_item_image_delete_one(request):
    image_id = request.GET.get('image_id')
    models.AuctionItemImage.objects.filter(id=image_id).delete()
    return JsonResponse({'status': True})


def coupon_list(request):
    """ 优惠券列表 """
    queryset = models.Coupon.objects.filter(deleted=False).order_by('-id')

    return render(request, 'web/coupon_list.html', {'queryset': queryset})


def coupon_add(request):
    if request.method == 'GET':
        form = CouponModelForm()
        return render(request, 'web/coupon_form.html', {'form': form})
    form = CouponModelForm(data=request.POST)
    if form.is_valid():
        instance = form.save()

        # 1.定时任务，从 未开始 到 领取中
        start_apply_datetime = datetime.datetime.utcfromtimestamp(form.instance.apply_start_date.timestamp())
        start_task_id = tasks.coupon_start_apply.apply_async(args=[instance.id], eta=start_apply_datetime).id

        # 2.定时任务，从 领取中 到 已结束
        start_apply_datetime = datetime.datetime.utcfromtimestamp(form.instance.apply_stop_date.timestamp())
        stop_task_id = tasks.coupon_stop_apply.apply_async(args=[instance.id], eta=start_apply_datetime).id

        instance.apply_start_task_id = start_task_id
        instance.apply_stop_task_id = stop_task_id
        instance.save()

        return redirect('coupon_list')
    return render(request, 'web/coupon_form.html', {'form': form})


def coupon_edit(request, pk):
    coupon_object = models.Coupon.objects.filter(id=pk, deleted=False).first()
    if not coupon_object or coupon_object.status != 1:
        return HttpResponse('优惠券不存在或优惠券已开始申请')

    if request.method == 'GET':
        form = CouponModelForm(instance=coupon_object)
        return render(request, 'web/coupon_form.html', {'form': form})

    form = CouponModelForm(instance=coupon_object, data=request.POST)
    if form.is_valid():
        if "apply_start_date" in form.changed_data:
            async_result = AsyncResult(id=coupon_object.apply_start_task_id, app=celery_app)
            async_result.revoke()
            eta = datetime.datetime.utcfromtimestamp(form.instance.apply_start_date.timestamp())
            start_task_id = tasks.coupon_start_apply.apply_async(args=[coupon_object.id], eta=eta).id
            form.instance.apply_start_task_id = start_task_id

        if "apply_stop_date" in form.changed_data:
            async_result = AsyncResult(id=coupon_object.apply_stop_task_id, app=celery_app)
            async_result.revoke()
            eta = datetime.datetime.utcfromtimestamp(form.instance.apply_stop_date.timestamp())
            start_task_id = tasks.coupon_stop_apply.apply_async(args=[coupon_object.id], eta=eta).id
            form.instance.apply_start_task_id = start_task_id

        form.save()
        return redirect('coupon_list')

    return render(request, 'web/coupon_form.html', {'form': form})


def coupon_delete(request, pk):
    """ 删除优惠券 """
    coupon_object = models.Coupon.objects.filter(id=pk, deleted=False).first()
    if not coupon_object:
        return JsonResponse({'status': False, 'error': '优惠券不存在'})

    start_result = AsyncResult(id=coupon_object.apply_start_task_id, app=celery_app)
    start_result.revoke()

    stop_result = AsyncResult(id=coupon_object.apply_stop_task_id, app=celery_app)
    stop_result.revoke()

    models.Coupon.objects.filter(id=pk, deleted=False).update(deleted=True)

    return JsonResponse({'status': True})
