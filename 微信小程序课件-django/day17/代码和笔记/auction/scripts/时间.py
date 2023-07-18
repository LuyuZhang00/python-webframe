#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 正确
import datetime
val = datetime.timedelta(minutes=1)

# 错误
from datetime import datetime
val = datetime.timedelta(minutes=1)