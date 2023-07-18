#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess

# result = subprocess.check_output('sh ls.sh', cwd='/Users/wupeiqi/project/bighg/script', shell=True)
# print(result.decode('utf-8'))


result = subprocess.check_output('rm -rf ls.sh', cwd='/Users/wupeiqi/project/bighg/script', shell=True)

