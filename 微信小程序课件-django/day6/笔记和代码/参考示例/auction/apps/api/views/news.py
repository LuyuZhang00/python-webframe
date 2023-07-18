#!/usr/bin/env python
# -*- coding:utf-8 -*-
import itertools
import collections
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from apps.api import models


# ################################ 动态列表 ################################

class CreateNewsTopicModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    cos_path = serializers.CharField()


class CreateNewsModelSerializer(serializers.ModelSerializer):
    imageList = CreateNewsTopicModelSerializer(many=True)

    class Meta:
        model = models.News
        exclude = ['user', 'viewer_count', 'comment_count']

    def create(self, validated_data):
        image_list = validated_data.pop('imageList')
        news_object = models.News.objects.create(**validated_data)
        data_list = models.NewsDetail.objects.bulk_create(
            [models.NewsDetail(**info, news=news_object) for info in image_list]
        )
        news_object.imageList = data_list

        if news_object.topic:
            news_object.topic.count += 1
            news_object.save()

        return news_object


class ListNewsModelSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        exclude = ['address', ]

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, ['id', 'title'])

    def get_user(self, obj):
        return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])


class ReachBottomFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('minId')
        if not min_id:
            return queryset
        return queryset.filter(id__lt=min_id)


class PullDownRefreshFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get('maxId')
        if not max_id:
            return queryset
        return queryset.filter(id__gt=max_id).reverse()


class NewsView(CreateAPIView, ListAPIView):
    """
    获取动态列表
    """
    queryset = models.News.objects.prefetch_related('user', 'topic').order_by("-id")

    filter_backends = [ReachBottomFilter, PullDownRefreshFilter]

    def perform_create(self, serializer):
        new_object = serializer.save(user_id=1)
        return new_object

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateNewsModelSerializer
        if self.request.method == 'GET':
            return ListNewsModelSerializer


# ################################ 动态详细 ################################


class RetrieveNewsDetailModelSerializerSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = models.News
        exclude = ['cover', ]

    def get_image_list(self, obj):
        return [model_to_dict(row, ['id', 'cos_path']) for row in obj.newsdetail_set.only('id', 'cos_path')]

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, ['id', 'title'])

    def get_user(self, obj):
        return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])

    def get_viewer(self, obj):
        queryset = models.ViewerRecord.objects.filter(news=obj).order_by('-id')
        view_object_list = queryset[0:10].values('user_id', 'user__avatar')

        mapping = {
            'user_id': 'id',
            'user__avatar': 'avatar'
        }
        context = {
            'count': queryset.count(),
            'result': [{mapping[key]: value for key, value in row.items()} for row in view_object_list]
        }
        return context

    def get_comment(self, obj):
        news_comment_queryset = models.CommentRecord.objects.filter(news=obj)
        total_count = news_comment_queryset.count()

        mapping = {
            'id': 'id',
            'content': 'content',
            'create_date': 'create_date',
            'depth': 'depth',
            'user__nickname': "nickname",
            'user__avatar': "avatar",
            'reply_id': 'reply',
            'reply__user__nickname': "reply_nickname"
        }
        # 获取前10条一级评论
        first_depth_queryset = news_comment_queryset.filter(depth=1).select_related('user', 'reply').order_by(
            '-id')[0:10].values(*mapping.keys())

        first_depth_dict = collections.OrderedDict()
        for row in first_depth_queryset:
            row['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M')
            row_dict = {mapping[key]: value for key, value in row.items()}
            first_depth_dict[row['id']] = row_dict

        # 获取所有相关的二级评论
        second_depth_queryset = news_comment_queryset.filter(depth=2, reply__in=first_depth_dict.keys()).select_related(
            'user', 'reply').order_by('id').values(*mapping.keys())
        second_depth_dict = {}
        for row in second_depth_queryset:
            row['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M')
            row_dict = {mapping[key]: value for key, value in row.items()}
            second_depth_dict[row['id']] = row_dict

            first_depth_dict[row_dict['reply']].setdefault('child', [])
            first_depth_dict[row_dict['reply']]['child'].append(row_dict)

        # 当前登录用户对获取相关的评论的赞记录（用于标记页面上赞按钮的状态）
        news_id = itertools.chain(first_depth_dict.keys(), second_depth_dict.keys())
        user_comment_favor_queryset = models.CommentFavorRecord.objects.filter(user_id=1, comment_id__in=news_id)
        for item in user_comment_favor_queryset:
            if item.comment_id in first_depth_dict:
                first_depth_dict[item.comment_id]['favor'] = True
            if item.comment_id in second_depth_dict:
                second_depth_dict[item.comment_id]['favor'] = True

        context = {
            'count': total_count,
            'result': first_depth_dict.values()
        }
        return context


class NewsDetailView(RetrieveAPIView):
    """
    获取动态详细
    """
    queryset = models.News.objects
    serializer_class = RetrieveNewsDetailModelSerializerSerializer


# ################################ 发布评论 ################################
"""
"id": 10,
"content": "哈哈哈哈",
"create_date": "2020-01-13 04:39",
"depth": 1,
"nickname": "wupeiqi",
"avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
"reply": null,
"reply_nickname": null,
"""


class CommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    reply_nickname = serializers.CharField(source='reply.user.nickname', read_only=True)

    class Meta:
        model = models.CommentRecord
        exclude = ["favor_count", "user"]

    def get_user(self, obj):
        return model_to_dict(obj.user, fields=['id', 'nickname', 'avatar'])


class CommentView(CreateAPIView):
    serializer_class = CommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=1)
