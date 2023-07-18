from django.db import models


# ############################### 动态 ###############################

class UserInfo(models.Model):
    telephone = models.CharField(verbose_name='手机号', max_length=11)
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    avatar = models.CharField(verbose_name='头像', max_length=64, null=True)
    token = models.CharField(verbose_name='用户Token', max_length=64)

    fans_count = models.PositiveIntegerField(verbose_name='粉丝个数', default=0)
    follow = models.ManyToManyField(verbose_name='关注', to='self', blank=True)

    balance = models.PositiveIntegerField(verbose_name='账户余额', default=1000)
    session_key = models.CharField(verbose_name='微信会话秘钥', max_length=32)
    openid = models.CharField(verbose_name='微信用户唯一标识', max_length=32)

    def __str__(self):
        return self.nickname


class Topic(models.Model):
    """
    话题
    """
    title = models.CharField(verbose_name='话题', max_length=32)
    count = models.PositiveIntegerField(verbose_name='关注度', default=0)


class News(models.Model):
    """
    动态
    """
    cover = models.CharField(verbose_name='封面', max_length=128)
    content = models.CharField(verbose_name='内容', max_length=255)
    topic = models.ForeignKey(verbose_name='话题', to='Topic', null=True, blank=True)
    address = models.CharField(verbose_name='位置', max_length=128, null=True, blank=True)

    user = models.ForeignKey(verbose_name='发布者', to='UserInfo', related_name='news')

    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)
    # favor = models.ManyToManyField(verbose_name='点赞记录', to='UserInfo', related_name="news_favor")

    viewer_count = models.PositiveIntegerField(verbose_name='浏览数', default=0)
    # viewer = models.ManyToManyField(verbose_name='浏览器记录', to='UserInfo', related_name='news_viewer')

    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ViewerRecord(models.Model):
    """
    浏览器记录
    """
    news = models.ForeignKey(verbose_name='动态', to='News')
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')


class NewsFavorRecord(models.Model):
    """
    动态赞记录表
    """
    news = models.ForeignKey(verbose_name='动态', to='News')
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo')


class CommentRecord(models.Model):
    """
    评论记录表
    """
    news = models.ForeignKey(verbose_name='动态', to='News')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo')
    create_date = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True)
    depth = models.PositiveIntegerField(verbose_name='评论层级', default=1)

    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)

    # 以后方便通过跟评论找到其所有的子孙评论
    root = models.ForeignKey(verbose_name='根评论', to='self', null=True, blank=True, related_name='descendant')


class CommentFavorRecord(models.Model):
    """
    评论赞记录
    """
    comment = models.ForeignKey(verbose_name='动态', to='CommentRecord')
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo')


class NewsDetail(models.Model):
    """
    动态详细
    """
    key = models.CharField(verbose_name='腾讯对象存储中的文件名', max_length=128, help_text="用于以后在腾讯对象存储中删除")
    cos_path = models.CharField(verbose_name='腾讯对象存储中图片路径', max_length=128)
    news = models.ForeignKey(verbose_name='动态', to='News')


# ############################### 拍卖 ###############################

class Auction(models.Model):
    """
    拍卖系列
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    status_choices = (
        (1, '未开拍'),
        (2, '预展中'),
        (3, '拍卖中'),
        (4, '已结束')
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    # cover = models.CharField(verbose_name='封面',max_length=128)
    cover = models.FileField(verbose_name='封面', max_length=128)

    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)

    preview_start_time = models.DateTimeField(verbose_name='预展开始时间')
    preview_end_time = models.DateTimeField(verbose_name='预展结束时间')

    auction_start_time = models.DateTimeField(verbose_name='拍卖开始时间')
    auction_end_time = models.DateTimeField(verbose_name='拍卖结束时间')

    deposit = models.PositiveIntegerField(verbose_name='全场保证金', default=1000)

    total_price = models.PositiveIntegerField(verbose_name='成交额', null=True, blank=True)
    goods_count = models.PositiveIntegerField(verbose_name='拍品数量', default=0)
    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '拍卖系列'

    def __str__(self):
        return self.title


class AuctionTask(models.Model):
    """ 定时任务 """
    auction = models.OneToOneField(verbose_name='专场', to='Auction')

    preview_task = models.CharField(verbose_name='Celery预展任务ID', max_length=64)

    auction_task = models.CharField(verbose_name='Celery拍卖任务ID', max_length=64)

    auction_end_task = models.CharField(verbose_name='Celery拍卖结束任务ID', max_length=64)


class AuctionItem(models.Model):
    """
    拍卖商品
    """
    auction = models.ForeignKey(verbose_name='拍卖', to='Auction')
    uid = models.CharField(verbose_name='图录号', max_length=12)
    title = models.CharField(verbose_name='拍品名称', max_length=32)
    status_choices = (
        (1, '未开拍'),
        (2, '预展中'),
        (3, '拍卖中'),
        (4, '成交'),
        (5, '流拍'),
        (6, '逾期未支付'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    cover = models.FileField(verbose_name='拍品封面', max_length=128)

    start_price = models.PositiveIntegerField(verbose_name='起拍价')
    deal_price = models.PositiveIntegerField(verbose_name='成交价', null=True, blank=True)

    reserve_price = models.PositiveIntegerField(verbose_name='参考底价')
    highest_price = models.PositiveIntegerField(verbose_name='参考高价')

    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)
    deposit = models.PositiveIntegerField(verbose_name='单品保证金', default=100)
    unit = models.PositiveIntegerField(verbose_name='加价幅度', default=100)

    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)

    class Meta:
        verbose_name_plural = '拍品'

    def __str__(self):
        return self.title


class AuctionItemImage(models.Model):
    """
    拍品详细图
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    img = models.FileField(verbose_name='详细图', max_length=64)
    carousel = models.BooleanField(verbose_name='是否在轮播中显示', default=False)
    order = models.FloatField(verbose_name="排序", default=1)

    class Meta:
        verbose_name_plural = '拍品详细图'

    def __str__(self):
        return "{}-{}".format(self.item.title, self.id, )


class AuctionItemDetail(models.Model):
    """
    拍品详细规格
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    key = models.CharField(verbose_name='项', max_length=16)
    value = models.CharField(verbose_name='值', max_length=32)

    class Meta:
        verbose_name_plural = '拍品规格'


class BrowseRecord(models.Model):
    """
    浏览记录
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')


class BidRecord(models.Model):
    """
    出价记录
    """
    status_choices = (
        (1, '竞价'),
        (2, '成交'),
        (3, '逾期未付款'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    user = models.ForeignKey(verbose_name='出价人', to='UserInfo')
    price = models.PositiveIntegerField(verbose_name='出价')


class DepositRecord(models.Model):
    """ 保证金 """
    status_choices = (
        (1, '未支付'),
        (2, '支付成功')
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    uid = models.CharField(verbose_name='流水号', max_length=64)
    deposit_type_choices = (
        (1, '单品保证金'),
        (2, '全场保证金')
    )
    deposit_type = models.SmallIntegerField(verbose_name='保证金类型', choices=deposit_type_choices)
    pay_type_choices = (
        (1, '微信'),
        (2, '余额')
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)

    amount = models.PositiveIntegerField(verbose_name='金额')  # 200
    balance = models.PositiveIntegerField(verbose_name='余额')  # 0

    user = models.ForeignKey(verbose_name='用户', to='UserInfo')

    # 单品保证金则设置值，全场保证金，则为空
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', null=True, blank=True)

    auction = models.ForeignKey(verbose_name='拍卖', to='Auction')


class Order(models.Model):
    """
    订单，拍卖结束时，执行定时任务处理：
        - 拍得，创建订单。
        - 未拍得，则退款到原账户
    """
    status_choices = (
        (1, '未支付'),
        (2, '待收货'),
        (3, '已完成'),
        (4, '逾期未支付'),
        (5, '支付中'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)

    uid = models.CharField(verbose_name='流水号', max_length=64)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    deposit = models.ForeignKey(verbose_name='保证金', to='DepositRecord')
    price = models.PositiveIntegerField(verbose_name='出价')

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    twenty_four_task_id = models.CharField(verbose_name='24小时后定时任务', max_length=32, null=True, blank=True)

    address = models.ForeignKey(verbose_name='收获地址', to='Address', null=True, blank=True)

    pay_type_choices = (
        (1, '微信'),
        (2, '余额')
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices,null=True, blank=True)
    real_price = models.PositiveIntegerField(verbose_name='实际支付金额', null=True, blank=True)


class DepositRefundRecord(models.Model):
    """ 保证金退款记录 """
    uid = models.CharField(verbose_name='流水号', max_length=64)
    status_choices = (
        (1, "待退款"),
        (2, '退款成功'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)
    deposit = models.ForeignKey(verbose_name='保证金', to='DepositRecord')
    amount = models.PositiveIntegerField(verbose_name='退款金额')


class DepositDeduct(models.Model):
    """ 扣除保证金 """
    order = models.ForeignKey(verbose_name='订单', to='Order')
    amount = models.PositiveIntegerField(verbose_name='金额')

    deduct_type_choices = (
        (1, '逾期扣款'),
        (2, '支付抵扣')
    )
    deduct_type = models.SmallIntegerField(verbose_name='扣款类型', choices=deduct_type_choices, default=1)


class Coupon(models.Model):
    """ 优惠券 """
    status_choices = (
        (1, '未开始'),
        (2, '领取中'),
        (3, '已结束')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    title = models.CharField(verbose_name='优惠券名称', max_length=32)
    auction = models.ForeignKey(verbose_name='专场', to='Auction')

    money = models.PositiveIntegerField(verbose_name='抵扣金额', default=200)

    count = models.PositiveIntegerField(verbose_name='创建数量', default=100)
    apply_count = models.PositiveIntegerField(verbose_name='已申请数量', default=0)

    apply_start_date = models.DateTimeField(verbose_name='开始领取时间')
    apply_stop_date = models.DateTimeField(verbose_name='领取结束时间')

    apply_start_task_id = models.CharField(verbose_name='celery任务ID', max_length=64, null=True, blank=True)
    apply_stop_task_id = models.CharField(verbose_name='celery任务ID', max_length=64, null=True, blank=True)

    deleted = models.BooleanField(verbose_name='是否删除', default=False)


class UserCoupon(models.Model):
    status_choices = (
        (1, '未使用'),
        (2, '已使用'),
        (3, '已过期')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    coupon = models.ForeignKey(verbose_name='优惠券', to='Coupon')
    order = models.ForeignKey(verbose_name='订单', to='Order', null=True, blank=True)


class Address(models.Model):
    """ 地址 """
    name = models.CharField(verbose_name='收货人姓名', max_length=32)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    detail = models.CharField(verbose_name='收货地址', max_length=255)

    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
