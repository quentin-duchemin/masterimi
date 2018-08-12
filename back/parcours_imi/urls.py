from django.urls import path, include
from rest_framework.routers import SimpleRouter

from parcours_imi import views
from parcours_imi.admin import user_parcours_import_view


router = SimpleRouter(trailing_slash=False)
router.register(r'courses', views.CourseViewSet)
router.register(r'masters', views.MasterViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/parcours_imi/userparcours/import', user_parcours_import_view, name='user_parcours_import'),
    path('api/', include(router.urls)),
]
