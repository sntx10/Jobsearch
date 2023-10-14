from django.contrib import admin

from apps.feedback.models import Favorite, UnwantedVacancy, UnwantedCompany, Subscription, Review

# Register your models here.

admin.site.register(Favorite)
admin.site.register(UnwantedVacancy)
admin.site.register(UnwantedCompany)
admin.site.register(Subscription)
admin.site.register(Review)
