from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.userprofile.models import UserProfile
from apps.userprofile.permissions import IsProfileOwner
from apps.userprofile.serializers import ProfileSerializer


# Create your views here.

class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            return UserProfile.objects.filter(user=user)
        else:
            return UserProfile.objects.none()
