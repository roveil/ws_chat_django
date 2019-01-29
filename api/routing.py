from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from api.ws_handler import ChatConsumer

asgi = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^chat/$", ChatConsumer),
        ])
    )
})
