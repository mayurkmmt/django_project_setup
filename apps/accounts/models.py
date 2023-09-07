from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from apps.common.models import TimeStampModel


class Company(TimeStampModel):
    company_name = models.CharField(max_length=100)
    company_email = models.EmailField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Companies"
        db_table = "companies"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
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


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=250)
    company = models.ForeignKey(
        "accounts.Company",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    user_type = models.IntegerField(blank=True, null=True, default=2)
    is_freeze = models.BooleanField(blank=True, null=True, default=False)
    verify_code = models.CharField(max_length=255, blank=True, null=True)
    verify_code_at = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_user_sso = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # required
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_company_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class RegistrationOtp(TimeStampModel):
    email = models.CharField(max_length=150, blank=True, null=True)
    otp = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        get_latest_by = ("created_at",)
