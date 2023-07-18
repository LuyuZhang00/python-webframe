from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import serializers
from api import models
from utils.filters import MinFilterBackend, MaxFilterBackend
from utils.pagination import OldBoyLimitPagination
from django.forms import model_to_dict
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from django.db.models import Max
from utils.auth import UserAuthentication
from rest_framework import exceptions
from django.db import transaction


class AuctionModelSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    preview_start_time = serializers.DateTimeField(format="%Y-%m-%d")

    goods = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        # fields = "__all__"
        fields = ['id', 'title', 'cover', 'status', 'preview_start_time',
                  'look_count', 'goods_count', 'total_price', 'bid_count', 'goods']

    def get_goods(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj)[0:5]
        return [row.cover for row in queryset]


# 专场列表
class AuctionView(ListAPIView):
    """ 拍卖专场接口 """
    queryset = models.Auction.objects.filter(status__gt=1).order_by('-id')
    serializer_class = AuctionModelSerializer
    filter_backends = [MinFilterBackend, MaxFilterBackend, ]
    pagination_class = OldBoyLimitPagination

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # 1.根据response.data获取所有的专场id id_list = [1,3,4,5]
        # 2.相关所有的单品  models.AuctionItem.objects.filter(auction_id__in=id_list)
        return response


class AuctionDetailItemModelSerializer(serializers.ModelSerializer):
    is_deposit = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = ['id', 'cover', 'status', 'reserve_price', 'highest_price', 'is_deposit']

    def get_is_deposit(self, obj):
        user_object = self.context['request'].user
        if not user_object:
            return False
        return models.DepositRecord.objects.filter(user=user_object, item=obj, status=2, deposit_type=1).exists()


class AuctionDetailModelSerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField()
    is_deposit = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = "__all__"

    def get_goods(self, obj):
        item_object_list = models.AuctionItem.objects.filter(auction=obj)
        ser = AuctionDetailItemModelSerializer(instance=item_object_list, many=True, context=self.context)
        return ser.data

    def get_is_deposit(self, obj):
        """ 检查是否已缴纳全场保证金 """
        # 1. 没登陆，显示去缴纳保证金
        user_object = self.context['request'].user
        if not user_object:
            return False
        # 2. 去查看缴纳保证金记录的表中是否有此用户&此专场
        return models.DepositRecord.objects.filter(user=user_object, auction=obj, status=2, item__isnull=True).exists()


# 专场详细
class AuctionDetailView(RetrieveAPIView):
    """ 专场详细（多个单品）"""
    queryset = models.Auction.objects.filter(status__gt=1)
    serializer_class = AuctionDetailModelSerializer


class AuctionItemDetailModelSerializer(serializers.ModelSerializer):
    carousel_list = serializers.SerializerMethodField()
    detail_list = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()
    record = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = "__all__"

    def get_carousel_list(self, obj):
        queryset = models.AuctionItemImage.objects.filter(item=obj, carousel=True).order_by('-order')
        return [row.img for row in queryset]

    def get_image_list(self, obj):
        queryset = models.AuctionItemImage.objects.filter(item=obj).order_by('-order')
        return [row.img for row in queryset]

    def get_detail_list(self, obj):
        queryset = models.AuctionItemDetail.objects.filter(item=obj)
        return [model_to_dict(row, ['key', 'value']) for row in queryset]

    def get_record(self, obj):
        queryset = models.BrowseRecord.objects.filter(item=obj)
        result = {
            'record_list': [row.user.avatar for row in queryset[0:10]],
            'total_count': queryset.count()
        }
        return result


# 单品详细
class AuctionItemDetailView(RetrieveAPIView):
    queryset = models.AuctionItem.objects.filter(status__gt=1)
    serializer_class = AuctionItemDetailModelSerializer


class AuctionDepositModelSerializer(serializers.ModelSerializer):
    deposit = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = ['id', 'title', 'cover', 'reserve_price', 'highest_price', 'deposit']

    def get_balance(self, obj):
        return self.context['request'].user.balance

    def get_deposit(self, obj):
        result = {
            "seleted": 1,
            'data_list': [
                {'id': 1, 'price': obj.deposit, 'text': '单品保证金'},
                {'id': 2, 'price': obj.auction.deposit, 'text': '全场保证金'},
            ]
        }
        return result


# 保证金(提交保证金)
class AuctionDepositView(RetrieveAPIView, CreateAPIView):
    authentication_classes = [UserAuthentication, ]
    queryset = models.AuctionItem.objects.filter(status__in=[2, 3])
    serializer_class = AuctionDepositModelSerializer


class BidModelSerializer(serializers.ModelSerializer):
    status_text = serializers.CharField(source='get_status_display', read_only=True)
    username = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = models.BidRecord
        fields = ['id', 'price', 'item', 'status_text', 'username']

    def validate_item(self, value):
        exists = models.AuctionItem.objects.filter(id=value, status=3).exists()
        if not exists:
            raise exceptions.ValidationError('已拍卖完成或未开拍')
        return value

    def validate_price(self, value):
        # value=用户提交的价格
        # 底价/加价幅度/最高价
        item_id = self.initial_data.get('item')
        item_object = models.AuctionItem.objects.filter(id=item_id).first()
        if value <= item_object.start_price:
            raise exceptions.ValidationError('不能低于起拍价')

        div = (value - item_object.start_price) % item_object.unit
        if div:
            raise exceptions.ValidationError('必须按照加价幅度来竞价')

        max_price = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price'))['max_price']
        if not max_price:
            return value

        if max_price >= value:
            raise exceptions.ValidationError('已经有人出这个价了，你再涨涨')
        return value


# 竞价    GET: http://www.xxx.com/deposit/?item_id=1
# 提交竞价 POST: http://www.xxx.com/deposit/
class BidView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthentication, ]
    queryset = models.BidRecord.objects.all().order_by('-id')
    serializer_class = BidModelSerializer

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        return self.queryset.filter(item_id=item_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        item_id = request.query_params.get('item_id')
        item_object = models.AuctionItem.objects.filter(id=item_id).first()

        max_price = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price'))['max_price']
        # {'max_price':1200}
        result = {
            'unit': item_object.unit,
            'price': max_price or item_object.start_price,
            'bid_list': response.data
        }
        response.data = result
        return response

    def perform_create(self, serializer):
        with transaction.atomic():
            price = self.request.data.get('price')
            item_id = self.request.data.get('item')
            result = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price')).select_for_update()
            max_price = result['max_price']
            if price > max_price:
                serializer.save(user=self.request.user)
            raise exceptions.ValidationError('已经被出价了，再涨涨.')


class Auction2View(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = models.Auction.objects.filter(status__gt=1).order_by('-id')
    serializer_class = AuctionModelSerializer
    filter_backends = [MinFilterBackend, MaxFilterBackend, ]
    pagination_class = OldBoyLimitPagination

    def get_serializer_class(self):
        pk = self.kwargs.get('pk')
        if pk:
            return AuctionDetailModelSerializer
        return AuctionModelSerializer
