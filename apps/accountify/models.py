from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.accountify.managers import UserManager


class User(AbstractUser):
    username = None
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=40, blank=True)
    can_create_company = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

