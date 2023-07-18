from django.conf.urls import url

from api.views import news
urlpatterns = [
    url(r'^topic/$', news.TopicView.as_view()),

    url(r'^news/$', news.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    url(r'^comment/$', news.CommentView.as_view()),
]