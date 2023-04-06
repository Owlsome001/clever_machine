from django.urls import path
from application.consumers import ApplicationConsumer
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({

})
ws_urlpatterns = [ 
    path('ws/teaching/', ApplicationConsumer.as_asgi())
]