from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from datetime import timedelta
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Creater(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Tasks(models.Model):
    """Db model that store taks information"""

    user = models.ForeignKey(Creater, on_delete=models.CASCADE, related_name="tasks")
    title = models.TextField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else self.description[:30]


class RequestedOtp(models.Model):
    """Used to store the hashed value of otp"""

    user = models.ForeignKey(Creater, on_delete=models.CASCADE, related_name="my_keys")
    hashed_text = models.CharField(max_length=256)
    expire_time = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.user.email}, {self.expire_time.date()}"

    def save(self, **kwargs):

        self.expire_time = timezone.now() + timedelta(minutes=5)
        return super().save(**kwargs)
