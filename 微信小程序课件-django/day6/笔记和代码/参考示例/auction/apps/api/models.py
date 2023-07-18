from django.db import models


# ############################### 动态 ###############################

class UserInfo(models.Model):
    telephone = models.CharField(verbose_name='手机号', max_length=11)
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    avatar = models.CharField(verbose_name='头像', max_length=64, null=True)
    token = models.CharField(verbose_name='用户Token', max_length=64)


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
    create_date = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True)
    depth = models.PositiveIntegerField(verbose_name='评论层级', default=1)

    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)


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

    status_choices = (
        ("ready", '未开拍'),
        ("preview", '预展中'),
        ("auction", '拍卖中'),
        ("stop", '已结束')
    )
    status = models.CharField(verbose_name='状态', choices=status_choices, default='ready', max_length=16)
    title = models.CharField(verbose_name='标题', max_length=32)
    img = models.CharField(verbose_name='拍卖图', max_length=64)
    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)

    preview_start_time = models.DateTimeField(verbose_name='预展开始时间')
    preview_end_time = models.DateTimeField(verbose_name='预展结束时间')

    auction_start_time = models.DateTimeField(verbose_name='拍卖开始时间')
    auction_end_time = models.DateTimeField(verbose_name='拍卖结束时间')

    total_price = models.PositiveIntegerField(verbose_name='成交额', null=True, blank=True)
    goods_count = models.PositiveIntegerField(verbose_name='拍品数量', default=0)
    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class AuctionItem(models.Model):
    """
    拍卖商品
    """
    auction = models.ForeignKey(verbose_name='拍卖', to='Auction')
    uid = models.CharField(verbose_name='图录号', max_length=12)

    status_choices = (
        (1, '未开拍'),
        (2, '拍卖中'),
        (3, '成交'),
        (4, '流拍'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    title = models.CharField(verbose_name='拍品名称', max_length=32)
    img = models.CharField(verbose_name='拍品图', max_length=64)
    deal_price = models.PositiveIntegerField(verbose_name='成交价', null=True, blank=True)
    reserve_price = models.PositiveIntegerField(verbose_name='参考底价')
    highest_price = models.PositiveIntegerField(verbose_name='参考高价')

    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)
    deposit = models.PositiveIntegerField(verbose_name='保证金')
    unit = models.PositiveIntegerField(verbose_name='加价幅度', default=100)

    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)


class AuctionItemDetail(models.Model):
    """
    拍品详细
    """
    img = models.CharField(verbose_name='详细图', max_length=64)
    carousel = models.BooleanField(verbose_name='是否在轮播中显示', default=False)
    order = models.FloatField(verbose_name="排序", default=1)


class BidRecord(models.Model):
    """
    出价记录
    """
    status_choices = (
        (1, '竞价'),
        (2, '成交'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    user = models.ForeignKey(verbose_name='出价人', to='UserInfo')
    price = models.PositiveIntegerField(verbose_name='出价')


class BrowseRecord(models.Model):
    """
    浏览记录
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem')
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
