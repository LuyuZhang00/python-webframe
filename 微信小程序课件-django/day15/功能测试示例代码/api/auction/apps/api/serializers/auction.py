#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from apps.api import models


class AuctionModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    cover = serializers.CharField()

    class Meta:
        model = models.Auction
        fields = ['id', 'title', 'status', 'cover', 'total_price', 'look_count', 'goods_count', 'items']

    def get_status(self, obj):
        status_class_mapping = {
            2: 'preview',
            3: 'auction',
            4: 'stop'
        }
        return {'text': obj.get_status_display(), 'class': status_class_mapping.get(obj.status)}

    def get_items(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj)[0:5]
        return [row.cover.name for row in queryset]


class AuctionDetailItemModelSerializer(serializers.ModelSerializer):
    cover = serializers.CharField()
    status_text = serializers.CharField(source='get_status_display')

    class Meta:
        model = models.AuctionItem
        fields = [
            'id', 'status', 'status_text', 'cover', 'unit', 'title', 'start_price',
            'deal_price', 'reserve_price', 'highest_price'
        ]


class AuctionDetailModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    deposit = serializers.SerializerMethodField(label='保证金')
    cover = serializers.CharField()

    class Meta:
        model = models.Auction
        fields = ['id', 'status', 'title', 'cover', 'look_count', 'goods_count', 'bid_count', 'items', 'deposit']

    def get_status(self, obj):
        status_class_mapping = {
            2: 'preview',
            3: 'auction',
            4: 'stop'
        }
        return {'text': obj.get_status_display(), 'class': status_class_mapping.get(obj.status)}

    def get_items(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj).exclude(status=1)
        ser = AuctionDetailItemModelSerializer(instance=queryset, many=True)
        return ser.data

    def get_deposit(self, obj):
        context = {
            'total': False,
            'single': {}
        }
        user_object = self.context['request'].user
        if not user_object:
            return context
        queryset = models.DepositRecord.objects.filter(user=user_object, auction=obj, status=2)
        if not queryset.exists():
            return context

        if queryset.filter(deposit_type=2).exists():
            context['total'] = True
            return context

        context['single'] = {row.item_id: True for row in queryset}
        return context
