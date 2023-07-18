#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
退款
根据订单号进行退款（需要使用证书才能操作）
文档：https://pay.weixin.qq.com/wiki/doc/api/H5.php?chapter=9_4&index=4
"""
import uuid
import random
import hashlib
import requests
from xml.etree import ElementTree as ET


def md5(string):
    ha = hashlib.md5()
    ha.update(string.encode('utf-8'))
    return ha.hexdigest()


def refund(trade_no, out_refund_no, total_fee, refund_fee):
    """
    订单号
    :param trade_no: 创建订单时自动生成的订单号
    :param out_refund_no: 商户退款单号
    :param total_fee: 订单金额
    :param refund_fee: 退款金额
    :return:
    """
    info = {
        'appid': 'wx55cca0b94f723dc7',
        'mch_id': '1526049051',
        'out_trade_no': trade_no,
        'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),
        'sign_type': "MD5",
        'out_refund_no': out_refund_no,
        'total_fee': total_fee,
        'refund_fee': refund_fee
    }
    key = "2SzCvaKgYExuItWBfYAqJFs72uUleD14"
    string = "&".join(["{0}={1}".format(k, info[k]) for k in sorted(info)] + ["{0}={1}".format("key", key, ), ])
    info['sign'] = md5(string).upper()

    xml = "<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in info.items()]))

    key = "xx/xxx/client_key.pem"
    cert = "xxx/xxx/xx/client_cert.pem"

    res = requests.post(
        url='https://api.mch.weixin.qq.com/secapi/pay/refund',
        data=xml.encode('utf-8'),
        headers={
            'Accept-Language': 'zh-CN,zh;q=0.9'
        },
        cert=(cert, key),
        verify=True
    )

    root = ET.XML(res.content.decode('utf-8'))
    response = {child.tag: child.text for child in root}
    if response['return_code'] == 'SUCCESS':
        return True


if __name__ == '__main__':
    out_refund_no = md5(str(uuid.uuid4()))
    print(out_refund_no)
    refund('8ccdbbd652d9ad12b82cf2b021669cb9', out_refund_no, 0.1, 0.1)
