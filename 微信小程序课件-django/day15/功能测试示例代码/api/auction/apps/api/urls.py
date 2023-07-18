#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from apps.api.views import auction
from apps.api.views import auth
from apps.api.views import topic
from apps.api.views import news
from apps.api.views import auction

urlpatterns = [
    url(r'^msg/', auth.MessageView.as_view()),
    url(r'^login/', auth.LoginView.as_view()),

    url(r'^oss/credential/$', auth.OssCredentialView.as_view()),

    # 话题
    url(r'^topic/$', topic.TopicView.as_view()),
    url(r'^news/$', news.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    url(r'^news/favor/$', news.NewsFavorView.as_view()),
    url(r'^comment/$', news.CommentView.as_view()),
    url(r'^comment/favor/$', news.CommentFavorView.as_view()),
    url(r'^follow/$', news.FollowView.as_view()),

    # 拍卖
    url(r'^auction/$', auction.AuctionView.as_view()),
    url(r'^auction/(?P<pk>\d+)/$', auction.AuctionDetailView.as_view()),

    url(r'^auction/deposit/(?P<pk>\d+)/$', auction.AuctionDepositView.as_view()),
    url(r'^pay/deposit/$', auction.PayDepositView.as_view()),
    url(r'^pay/deposit/notify/$', auction.PayDepositNotifyView.as_view()),

    url(r'^bid/$', auction.BidView.as_view()),
]
