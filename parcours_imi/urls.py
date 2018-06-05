from django.urls import path, include
from rest_framework.routers import DefaultRouter

from parcours_imi import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'masters', views.MasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
