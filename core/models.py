from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None

    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("admin", "Admin"),
        ("fpo", "FPO"),
    ]

    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="farmer")
    address = models.TextField(blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"


class Farm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farms")
    location = models.CharField(max_length=255)
    size = models.FloatField(help_text="Area in acres")
