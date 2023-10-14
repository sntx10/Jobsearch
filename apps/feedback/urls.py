from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.feedback.views import FavoriteAPIView, UnwantedAPIView, CompanyUnwantedAPIView, \
    SubscriptionAPIView, ReviewAPIView

router = DefaultRouter()
router.register('favourite', FavoriteAPIView)
router.register('unwanted', UnwantedAPIView)
router.register('unwanted/company', CompanyUnwantedAPIView)
router.register('subscription', SubscriptionAPIView)
router.register('reviews', ReviewAPIView)

urlpatterns = [
    path('', include(router.urls))
]