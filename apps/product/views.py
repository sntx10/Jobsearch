from datetime import datetime, timedelta
from functools import reduce

import django_filters
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import ModelMultipleChoiceFilter
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import SpecializationSubType, CompanyIndustrySubType, Company, Recruiter
from apps.catalog.serializers import RecruiterSerializer
from apps.feedback.models import UnwantedCompany, UnwantedVacancy
from apps.product.models import Vacancy, Resume
from apps.product.permissions import IsOwnerOrReadOnly, CanCreateCompany, IsRecruiterWithPermission
from apps.product.serializers import ResumeSerializer, VacancySerializer, VacancyDetailSerializer, \
    ResumeListSerializer, ResumeDetailSerializer, ResumeUpdateSerializer, CompanySerializer, VacancyCreateSerializer, \
    CompanyDetailSerializer, CompanyListSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SpecializationFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')

    subtype = ModelMultipleChoiceFilter(
        field_name='specialization_type__name',
        queryset=SpecializationSubType.objects.all(),
        to_field_name='name',
        label='Выберите специализацию'
    )

    company_subtype = ModelMultipleChoiceFilter(
        field_name='company_subtype__company_type__name__company__name',
        queryset=CompanyIndustrySubType.objects.all(),
        to_field_name='name',
        label='Отрасль Компании'
    )

    def filter_location(self, queryset, name, value):
        return queryset.filter(location__contains=value)

    class Meta:
        model = Vacancy
        fields = ['subtype', 'company', 'company_subtype', 'city', 'location']


class CityFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')

    def filter_location(self, queryset, name, value):
        return queryset.filter(location__contains=value)

    class Meta:
        model = Resume
        fields = ['city', 'location']


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Company
        fields = ['name']


@method_decorator(cache_page(60 * 15), name='dispatch')
class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_class = SpecializationFilter
    pagination_class = LargeResultsSetPagination
    search_fields = ['title', 'company__name', 'specialization__name']


class VacancyCreateAPIView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsRecruiterWithPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class VacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    lookup_field = 'id'


class VacancyUpdateAPIView(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class VacancyDeleteAPIView(generics.DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    # permission_classes = [IsOwnerOrReadOnly]


@method_decorator(cache_page(60 * 15), name='dispatch')
class ResumeListAPIView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeListSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filterset_class = CityFilter
    search_fields = ['title', 'skills__title', 'specialization__name']


@method_decorator(cache_page(60 * 15), name='dispatch')
class ResumeDetailAPIView(generics.RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeDetailSerializer
    lookup_field = 'id'


class ResumeCreateAPIView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeUpdateAPIView(generics.UpdateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUpdateSerializer
    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ResumeDeleteAPIView(generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = CompanyFilter
    search_fields = ['name']


@method_decorator(cache_page(60 * 15), name='dispatch')
class CompanyDetailAPIView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [CanCreateCompany]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecruiterCreateAPIView(generics.CreateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = [CanCreateCompany]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecruiterDeleteAPIView(generics.DestroyAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = [CanCreateCompany]


class RecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        latest_vacancies = Vacancy.objects.filter(created_at__gte=datetime.now()-timedelta(days=180)).order_by('-created_at')[:5]
        if len(latest_vacancies) < 10:
            latest_vacancies = Vacancy.objects.filter(created_at__gte=datetime.now()-timedelta(days=180))

        unwanted_companies = UnwantedCompany.objects.filter(user=user).values_list('company', flat=True)

        unwanted_vacancies = UnwantedVacancy.objects.filter(user=user).values_list('vacancy', flat=True)

        vacancy_list = Vacancy.objects.all()

        if unwanted_vacancies:
            vacancy_list = vacancy_list.exclude(id__in=unwanted_vacancies)

        if unwanted_companies:
            vacancy_list = vacancy_list.exclude(reduce(lambda x, y: x | y, [Q(company=company)
                                                                            for company in unwanted_companies]))

        vacancy_list = vacancy_list.order_by('-created_at')

        if len(vacancy_list) < 10:
            serializer = VacancySerializer(vacancy_list, many=True)
            return Response(serializer.data)

        recommend_vacancies = vacancy_list[:10]

        serializer = VacancySerializer(recommend_vacancies, many=True)
        return Response(serializer.data)
