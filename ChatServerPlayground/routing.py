from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
from channels.http import AsgiHandler
from token_auth import TokenAuthMiddlewareStack


from chat.consumers import ChatConsumer
from public_chat.consumers import PublicChatConsumer
from notification.consumers import NotificationConsumer


application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
			path('', NotificationConsumer),
			path('chat/<room_id>/', ChatConsumer),
			path('public_chat/<room_id>/', PublicChatConsumer),			
        ]),
    ),
})