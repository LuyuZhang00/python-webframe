#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
from django.forms import ModelForm
from django.forms import widgets as wds
from django.db.models.fields.files import FieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from apps.api import models
from utils.tencent.cos import upload_file

from .bootstrap import BootStrapModelForm


class AuctionModelForm(BootStrapModelForm):
    exclude_bootstrap_class = ['cover']

    class Meta:
        model = models.Auction
        exclude = ['total_price', 'status', 'goods_count', 'bid_count', 'look_count', 'video']

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('cover')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data

        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['cover'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class AuctionItemAddModelForm(BootStrapModelForm):
    exclude_bootstrap_class = ['cover']

    class Meta:
        model = models.AuctionItem
        exclude = ['auction', 'uid', 'deal_price', 'video', 'bid_count', 'look_count']

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('cover')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data
        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['cover'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class AuctionItemEditModelForm(BootStrapModelForm):
    exclude_bootstrap_class = ['cover']

    class Meta:
        model = models.AuctionItem
        exclude = ['auction', 'uid', 'deal_price', 'video', 'bid_count', 'look_count']

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('cover')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data
        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['cover'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class AuctionDetailModelForm(ModelForm):
    class Meta:
        model = models.AuctionItemDetail
        exclude = ['item']


class AuctionItemImageModelForm(BootStrapModelForm):
    class Meta:
        model = models.AuctionItemImage
        exclude = ['item', 'order']

    def clean_carousel(self):
        value = self.cleaned_data.get('carousel')
        return bool(value)

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('img')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data

        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['img'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class CouponModelForm(BootStrapModelForm):
    class Meta:
        model = models.Coupon
        exclude = ['status', 'apply_count', 'apply_start_task_id', 'apply_stop_task_id', 'deleted']
