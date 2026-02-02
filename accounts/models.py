# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        blank=True,
        null=True
    )
    # We'll keep first_name, last_name from AbstractUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still needed for createsuperuser

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(
        max_length=20,
        choices=[
            ('HOME', 'Home'),
            ('WORK', 'Work'),
            ('OTHER', 'Other'),
        ],
        default='HOME'
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=150)       # area/street/locality
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=150, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.address_type} - {self.city}"