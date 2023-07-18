#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url

from apps.web.views import auction

urlpatterns = [

    url(r'^auction/list/$', auction.auction_list, name='auction_list'),
    url(r'^auction/add/$', auction.auction_add, name='auction_add'),
    url(r'^auction/delete/(?P<pk>\d+)/$', auction.auction_delete, name='auction_delete'),
    url(r'^auction/edit/(?P<pk>\d+)/$', auction.auction_edit, name='auction_edit'),

    url(r'^auction/item/list/(?P<auction_id>\d+)/$', auction.auction_item_list, name='auction_item_list'),
    url(r'^auction/item/add/(?P<auction_id>\d+)/$', auction.auction_item_add, name='auction_item_add'),
    url(r'^auction/item/edit/(?P<auction_id>\d+)/(?P<item_id>\d+)/$', auction.auction_item_edit, name='auction_item_edit'),
    url(r'^auction/item/delete/(?P<item_id>\d+)/$', auction.auction_item_delete, name='auction_item_delete'),

    url(r'^auction/item/detail/add/(?P<item_id>\d+)/$', auction.auction_item_detail_add, name='auction_item_detail_add'),
    url(r'^auction/item/detail/add/one/(?P<item_id>\d+)/$', auction.auction_item_detail_add_one, name='auction_item_detail_add_one'),
    url(r'^auction/item/detail/delete/one/$', auction.auction_item_detail_delete_one, name='auction_item_detail_delete_one'),

    url(r'^auction/item/image/add/(?P<item_id>\d+)/$', auction.auction_item_image_add, name='auction_item_image_add'),
    url(r'^auction/item/image/add/one/(?P<item_id>\d+)/$', auction.auction_item_image_add_one, name='auction_item_image_add_one'),
    url(r'^auction/item/image/delete/one/$', auction.auction_item_image_delete_one, name='auction_item_image_delete_one'),

    url(r'^coupon/list/$', auction.coupon_list, name='coupon_list'),
    url(r'^coupon/add/$', auction.coupon_add, name='coupon_add'),
    url(r'^coupon/edit/(?P<pk>\d+)/$', auction.coupon_edit, name='coupon_edit'),
    url(r'^coupon/delete/(?P<pk>\d+)/$', auction.coupon_delete, name='coupon_delete'),

]
