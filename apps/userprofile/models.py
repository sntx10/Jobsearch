from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _

# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    education = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', default='profile_pictures/default.png')
    private_email = models.BooleanField(default=True)
    private_number = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        super().clean()
        if self.phone_number and not re.match(r'^\+?[0-9]+$', self.phone_number):
            self.add_error('phone_number', _('Please enter a valid phone number'))
            raise ValidationError(_('Invalid phone number format'))

    def save(self, *args, **kwargs):
        if not self.first_name and not self.last_name:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print(f"User {instance.email} was created: {created}")
    if created:
        UserProfile.objects.create(user=instance)
