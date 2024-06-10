from django.urls import path
from django.conf import settings
from .views import handle_webhook_requests
urlpatterns = [
    path(settings.BOT_TOKEN, handle_webhook_requests)
]