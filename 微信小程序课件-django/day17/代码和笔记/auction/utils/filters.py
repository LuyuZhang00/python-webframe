#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.filters import BaseFilterBackend


class ReachBottomFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('minId')
        if not min_id:
            return queryset
        return queryset.filter(id__lt=min_id)


class PullDownRefreshFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get('maxId')
        if not max_id:
            return queryset
        return queryset.filter(id__gt=max_id).reverse()


class BidItemFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        item_id = request.query_params.get('item_id')
        if not item_id:
            return queryset.none
        return queryset.filter(item_id=item_id)
