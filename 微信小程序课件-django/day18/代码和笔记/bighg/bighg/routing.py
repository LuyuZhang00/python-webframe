from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.sessions import CookieMiddleware,SessionMiddlewareStack
from apps.web import consumers


application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(URLRouter([
        url(r'^deploy/(?P<task_id>\d+)/$', consumers.DeployConsumer),
    ]))
})