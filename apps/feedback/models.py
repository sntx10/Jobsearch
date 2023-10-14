from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.product.models import Vacancy, Company

# from apps.catalog.models import Company
# from apps.product.models import Vacancy

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user}'


class UnwantedVacancy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vc_unwanted')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vc_unwanted')

    def __str__(self):
        return f'{self.user}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f'{self.user}'


class UnwantedCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cm_unwanted')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cm_unwanted')

    def __str__(self):
        return f'{self.user}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


