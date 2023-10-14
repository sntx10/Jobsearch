from django.contrib import admin

from apps.chat.models import Room, Chat

# Register your models here.


admin.site.register(Room)
admin.site.register(Chat)
