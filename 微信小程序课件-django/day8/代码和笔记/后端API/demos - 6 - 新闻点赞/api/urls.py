from django.conf.urls import url

from api.views import news
from api.views import auth
urlpatterns = [
    url(r'^message/', auth.MessageView.as_view()),
    url(r'^login/', auth.LoginView.as_view()),


    url(r'^topic/$', news.TopicView.as_view()),
    url(r'^news/$', news.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    url(r'^comment/$', news.CommentView.as_view()),
    url(r'^favor/$', news.FavorView.as_view()),

    url(r'^test/$', news.TestView.as_view()),

]