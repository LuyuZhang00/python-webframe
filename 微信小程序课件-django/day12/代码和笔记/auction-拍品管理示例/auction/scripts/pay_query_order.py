#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
查看订单状态
根据订单号查询微信支付订单状态
文档：https://pay.weixin.qq.com/wiki/doc/api/H5.php?chapter=9_2&index=2
"""
import random
import hashlib
import requests
from xml.etree import ElementTree as ET


def md5(string):
    ha = hashlib.md5()
    ha.update(string.encode('utf-8'))
    return ha.hexdigest()


def func(trade_no):
    """
    订单号
    :param trade_no: 创建订单时自动生成的订单号
    :return:
    """
    info = {
        'appid': 'wx55cca0b94f723dc7',
        'mch_id': '1526049051',  # 商户号
        'out_trade_no': trade_no,
        'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),
        'sign_type': "MD5",

    }
    key = "2SzCvaKgYExuItWBfYAqJFs72uUleD14"
    string = "&".join(["{0}={1}".format(k, info[k]) for k in sorted(info)] + ["{0}={1}".format("key", key, ), ])
    info['sign'] = md5(string).upper()

    xml = "<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in info.items()]))
    res = requests.post('https://api.mch.weixin.qq.com/pay/orderquery', data=xml.encode('utf-8'))

    root = ET.XML(res.content.decode('utf-8'))
    result = {child.tag: child.text for child in root}
    print(result)


if __name__ == '__main__':
    func('8ccdbbd652d9ad12b82cf2b021669cb9')
