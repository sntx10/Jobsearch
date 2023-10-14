from django.contrib import admin

from apps.accountify.models import User
from apps.userprofile.models import UserProfile

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)