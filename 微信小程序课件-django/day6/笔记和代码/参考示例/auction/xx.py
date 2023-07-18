#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

pool = redis.ConnectionPool(host='10.211.55.25', port=6379)
conn = redis.Redis(connection_pool=pool)
print(conn.keys())
