from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUserType(models.Model):
    """
    This model corresponds to the nekretnine_customuser_type table.
    """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "nekretnine_customuser_type"  # match your existing table name
        verbose_name = "User type"
        verbose_name_plural = "User type"

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    user_type = models.ForeignKey(
        CustomUserType,
        on_delete=models.CASCADE,
        null=True,  # or false if you want to enforce a user type always
        blank=True
    )
    email = models.EmailField(unique=True)  # Override to make it unique
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    consent = models.BooleanField(default=False)  # Consent tracking
    image_url = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Change this field type

    # Remove first_name and last_name if you prefer full_name
    full_name = models.CharField(max_length=255, blank=True, null=True)

    # Field for storing image URL
    image_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Korisnik"
        verbose_name_plural = "Korisnici"

    def __str__(self):
        return self.email


class SuperUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=True)

class SuperUser(CustomUser):
    objects = SuperUserManager()

    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
