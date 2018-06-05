from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views

from parcours_imi import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'masters', views.MasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', authtoken_views.obtain_auth_token)
]
