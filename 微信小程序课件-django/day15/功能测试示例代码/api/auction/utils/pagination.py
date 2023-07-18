#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class RollLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50

    def get_offset(self, request):
        return 0

    def get_paginated_response(self, data):
        return Response(data)
