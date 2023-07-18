from django.db import models

class UserInfo(models.Model):
    """
    用户表
    """
    phone = models.CharField(verbose_name='手机号',max_length=32)
    token = models.CharField(verbose_name='Token',max_length=32)
    openid = models.CharField(verbose_name='微信唯一标识',max_length=32)


class Goods(models.Model):
    """ 商品表 """
    title = models.CharField(verbose_name='商品名称',max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')


class Order(models.Model):
    """ 订单表 """
    status_choices = (
        (1,'待支付'),
        (2,'已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态',choices=status_choices)
    goods = models.ForeignKey(verbose_name='商品',to='Goods')
    user =  models.ForeignKey(verbose_name='用户',to='UserInfo')

    uid = models.CharField(verbose_name='订单号',max_length=64)


