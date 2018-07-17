from django.urls import path, include
from rest_framework.routers import SimpleRouter

from messaging import views

router = SimpleRouter(trailing_slash=False)
router.register(r'conversations', views.ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
