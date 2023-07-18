#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import BaseFilterBackend

class AuctionView(APIView):

    def get(self, request, *args, **kwargs):
        max_auction_id = request.query_params.get('maxAuctionId')
        if max_auction_id:
            new_auction_list = [
                {
                    "id": 5,
                    "title": "第五场 贵和祥茶道专场",
                    "status": "preview",
                    "status_text": "预展中",
                    "look_count": 390,
                    "img": "/static/images/auction/lg.png",
                    "goods_count": 14,
                    "total_price": 59000,
                    "pics": [
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png"
                    ]
                }, {
                    "id": 4,
                    "title": "第四场 贵和祥茶道专场",
                    "status": "preview",
                    "status_text": "预展中",
                    "look_count": 390,
                    "img": "/static/images/auction/lg.png",
                    "goods_count": 14,
                    "total_price": 59000,
                    "pics": [
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png",
                        "/static/images/auction/lg.png"
                    ]
                }
            ]

            return Response(new_auction_list)
        new_auction_list = [
            {
                "id": 3,
                "title": "第三场 贵和祥茶道专场",
                "status": "preview",
                "status_text": "预展中",
                "look_count": 390,
                "img": "/static/images/auction/lg.png",
                "goods_count": 14,
                "total_price": 59000,
                "pics": [
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png"
                ]
            }, {
                "id": 2,
                "title": "第二场 贵和祥茶道专场",
                "status": "auction",
                "status_text": "拍卖中",
                "look_count": 390,
                "img": "/static/images/auction/lg.png",
                "goods_count": 14,
                "total_price": 59000,
                "pics": [
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png"
                ]
            },
            {
                "id": 1,
                "title": "第一场 贵和祥茶道专场",
                "status": "stop",
                "status_text": "已结束",
                "look_count": 390,
                "img": "/static/images/auction/lg.png",
                "goods_count": 14,
                "total_price": 59000,
                "pics": [
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png",
                    "/static/images/auction/lg.png"
                ]
            },
        ]
        return Response(new_auction_list)


