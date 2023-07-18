#!/usr/bin/env python
# -*- coding:utf-8 -*-


class BaseResponse(object):
    def __init__(self, status=False, data=None, message=None):
        self.status = status
        self.data = data
        self.message = message

    @property
    def dict(self):
        return self.__dict__
