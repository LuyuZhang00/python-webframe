#!/usr/bin/env python
# -*- coding:utf-8 -*-
from apps.api import models
from rest_framework.permissions import BasePermission


class BidPermission(BasePermission):
    def has_permission(self, request, view):
        """
        校验是否具有权限，当前用户如果未付保证金，则无权访问
        """
        item_id = request.query_params.get('item_id')
        item_object = models.AuctionItem.objects.filter(id=item_id).first()
        if not item_object:
            return

        item_exists = models.DepositRecord.objects.filter(deposit_type=1, user=request.user, item_id=item_id, status=2,
                                                          item__status=3).exists()
        if item_exists:
            return item_exists

        auction_exists = models.DepositRecord.objects.filter(deposit_type=2,
                                                             user=request.user, auction=item_object.auction, status=2,
                                                             auction__status=3).exists()
        if auction_exists:
            return auction_exists

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
