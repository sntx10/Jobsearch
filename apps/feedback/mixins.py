from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.feedback.models import Favorite, UnwantedVacancy, UnwantedCompany, Subscription, Review
from apps.feedback.serializers import ReviewSerializer


class SubscriptionMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        try:
            obj = Subscription.objects.get(company_id=pk, user=request.user)
            obj.delete()
            status_ = 'Вы отписались'
        except Subscription.DoesNotExist:
            obj = Subscription.objects.create(company_id=pk, user=request.user)
            status_ = 'Вы подписались'
        return Response({'msg': status_})


class FavoriteMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        try:
            obj = Favorite.objects.get(vacancy_id=pk, user=request.user)
            obj.delete()
            status_ = 'Удалено из избранного'
        except Favorite.DoesNotExist:
            obj = Favorite.objects.create(vacancy_id=pk, user=request.user)
            status_ = 'Добавлено в избранное'
        return Response({'msg': status_})


class UnwantedVacancyMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        try:
            obj = UnwantedVacancy.objects.get(vacancy_id=pk, user=request.user)
            obj.delete()
            status_ = 'Вакансия удалено из нежелательных'
        except UnwantedVacancy.DoesNotExist:
            obj = UnwantedVacancy.objects.create(vacancy_id=pk, user=request.user)
            status_ = 'Вакансия добавлено в нежелательное'
        return Response({'msg': status_})


class UnwantedCompanyMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        try:
            obj = UnwantedCompany.objects.get(company_id=pk, user=request.user)
            obj.delete()
            status_ = 'Компания удалено из нежелательных'
        except UnwantedCompany.DoesNotExist:
            obj = UnwantedCompany.objects.create(company_id=pk, user=request.user)
            status_ = 'Компания добавлено в нежелательное'
        return Response({'msg': status_})


class ReviewsMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Review.objects.get_or_create(vacancy_id=pk, user=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

