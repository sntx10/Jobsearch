from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.userprofile import views

router = DefaultRouter()
router.register("", views.ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]