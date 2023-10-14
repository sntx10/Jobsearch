from django.shortcuts import render
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from apps.feedback.mixins import FavoriteMixin, SubscriptionMixin,\
    ReviewsMixin, UnwantedVacancyMixin, UnwantedCompanyMixin
from apps.feedback.models import Favorite, UnwantedCompany, UnwantedVacancy, Subscription, Review
from apps.feedback.permissions import IsFavoriteOwner
from apps.feedback.serializers import FavoriteSerializer, UnwantedSerializer, CompanyUnwantedSerializer, \
    SubscriptionSerializer, ReviewSerializer


class FavoriteAPIView(mixins.ListModelMixin,  FavoriteMixin, GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsFavoriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class UnwantedAPIView(mixins.ListModelMixin, UnwantedVacancyMixin, GenericViewSet):
    queryset = UnwantedVacancy.objects.all()
    serializer_class = UnwantedSerializer
    permission_classes = [IsFavoriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class CompanyUnwantedAPIView(mixins.ListModelMixin, UnwantedCompanyMixin, GenericViewSet):
    queryset = UnwantedCompany.objects.all()
    serializer_class = CompanyUnwantedSerializer
    permission_classes = [IsFavoriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class SubscriptionAPIView(mixins.ListModelMixin, SubscriptionMixin, GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsFavoriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ReviewAPIView(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                    ReviewsMixin, GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset