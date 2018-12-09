from django.urls import path, include
from rest_framework.routers import SimpleRouter

from parcours_imi import views
from parcours_imi.admin import user_parcours_export_view, user_parcours_import_view, user_parcours_reset_view


router = SimpleRouter(trailing_slash=False)
router.register(r'courses', views.CourseViewSet)
router.register(r'masters', views.MasterViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/parcours_imi/userparcours/export', user_parcours_export_view, name='user_parcours_export'),
    path('admin/parcours_imi/userparcours/import', user_parcours_import_view, name='user_parcours_import'),
    path('admin/parcours_imi/userparcours/<path:object_id>/reset', user_parcours_reset_view, name='user_parcours_reset'),
    path('api/', include(router.urls)),
]
