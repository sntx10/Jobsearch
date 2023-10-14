from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include


router = DefaultRouter()
# router.register('resume', views.ResumeViewSet, basename='resume')
# router.register('vacancy', views.VacancyViewSet, basename='vacancy')

urlpatterns = [
    path('recommendation/', views.RecommendationView.as_view(), name='recommends'),
    path('vacancies/', views.VacancyListAPIView.as_view(), name='vacancy-list'),
    path('vacancy/<int:id>/', views.VacancyDetailAPIView.as_view(), name='vacancy-detail'),
    path('vacancy/update/<int:id>', views.VacancyUpdateAPIView.as_view(), name='vacancy-update'),
    path('vacancy/delete/<int:id>', views.VacancyDeleteAPIView.as_view(), name='vacancy-delete'),
    path('vacancy/create/', views.VacancyCreateAPIView.as_view(), name='vacancy-create'),
    path('resume/', views.ResumeListAPIView.as_view(), name='resume'),
    path('resume/<int:id>/', views.ResumeDetailAPIView.as_view(), name='resume-detail'),
    path('resume/update/<int:pk>', views.ResumeUpdateAPIView.as_view(), name='resume-update'),
    path('resume/delete/<int:pk>', views.ResumeDeleteAPIView.as_view(), name='resume-delete'),
    path('resume/create/', views.ResumeCreateAPIView.as_view(), name='resume-create'),
    path('companies/', views.CompanyListAPIView.as_view(), name='companies-list'),
    path('company/<int:pk>/', views.CompanyDetailAPIView.as_view(), name='company-detail'),
    path('company/create/', views.CompanyCreateAPIView.as_view(), name='company-create'),
    path('recruiter/create/', views.RecruiterCreateAPIView.as_view(), name='recruiter-create'),
    path('recruiter/delete/', views.RecruiterDeleteAPIView.as_view(), name='recruiter-delete'),
    path('', include(router.urls)),
]
