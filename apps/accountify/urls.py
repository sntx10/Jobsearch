from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name='register'),
    path("confirm/<uuid:activation_code>/", views.ActivationAPIView.as_view(), name='activation_code'),
    path("change/password/", views.ChangePasswordAPIView.as_view(), name='change_password'),
    path("delete/account/", views.DeleteAccountAPIView.as_view(), name='delete_account'),

    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),
]
