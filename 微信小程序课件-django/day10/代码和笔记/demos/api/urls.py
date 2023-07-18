from django.conf.urls import url

from api.views import news
from api.views import auth
from api.views import task
from api.views import auction
urlpatterns = [
    url(r'^message/', auth.MessageView.as_view()),
    url(r'^login/', auth.LoginView.as_view()),


    url(r'^topic/$', news.TopicView.as_view()),
    url(r'^news/$', news.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    url(r'^comment/$', news.CommentView.as_view()),
    url(r'^favor/$', news.FavorView.as_view()),

    # celery示例
    url(r'^create/task/$', task.create_task),
    url(r'^get/result/$', task.get_result),

    # 专场列表
    url(r'^auction/$', auction.AuctionView.as_view()),
    url(r'^auction/(?P<pk>\d+)/$', auction.AuctionDetailView.as_view()),
    url(r'^auction/item/(?P<pk>\d+)/$', auction.AuctionItemDetailView.as_view()),

    url(r'^auction/deposit/(?P<pk>\d+)/$', auction.AuctionDepositView.as_view()),

    url(r'^bid/$', auction.BidView.as_view()),


    url(r'^auction2/$', auction.Auction2View.as_view({'get':'list'})),
    url(r'^auction2/(?P<pk>\d+)/$', auction.Auction2View.as_view({'get':'retrieve'})),
]














