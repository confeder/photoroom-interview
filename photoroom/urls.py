from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from . import views
from .admin import admin_site

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"teams", views.TeamViewSet, basename="team")
router.register(r"palletes", views.ColorPalleteViewSet, basename="palletes")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path(
        "api/docs/", include_docs_urls(title="Photoroom Color Palletes API", public=True)
    ),
    path("admin/", admin_site.urls),
]
