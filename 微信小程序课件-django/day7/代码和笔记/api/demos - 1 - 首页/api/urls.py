from django.conf.urls import url

from api.views import news
urlpatterns = [
    url(r'^news/$', news.NewsView.as_view()),
    url(r'^topic/$', news.TopicView.as_view()),
]