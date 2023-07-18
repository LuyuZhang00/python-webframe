#!/usr/bin/env python
# -*- coding:utf-8 -*-
import itertools

v1 = {1: 'alex'}
v2 = {33: '武沛齐'}

result = itertools.chain(v1.keys(), v2.keys())
for item in result:
    print(item)
