from django.urls import include, path
from rest_framework import routers

from . import views
from .admin import admin_site

router = routers.DefaultRouter()
router.register(r"teams", views.TeamViewSet, basename="team")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include(router.urls)),
    path("admin/", admin_site.urls),
]
