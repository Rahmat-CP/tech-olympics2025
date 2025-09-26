from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import RegexValidator
from django.db import models


# ============================ Dont Remove Previous Models ================================

class AdminUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    national_id = models.CharField(max_length=10)
    address = models.TextField()
    admin_code = models.CharField(max_length=10)
    permissions_json = models.TextField()
    status = models.CharField(max_length=20, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)


class CustomerUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    national_id = models.CharField(max_length=10)
    address = models.TextField()
    zipcode = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    loyalty_points = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)


class VendorUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    national_id = models.CharField(max_length=10)
    address = models.TextField()
    shop_name = models.CharField(max_length=150)
    shop_address = models.TextField()
    shop_license_number = models.CharField(max_length=50)
    shop_phone = models.CharField(max_length=20)
    rating = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)

# ============================ Dont Remove Previous Models ================================

class CustomUser(AbstractUser):
    # TODO: Implement Model CustomUser
    pass


class AdminProfile(models.Model):
    # TODO: Implement Model AdminProfile
    pass


class CustomerProfile(models.Model):
    # TODO: Implement Model CustomerProfile
    pass


class VendorProfile(models.Model):
    # TODO: Implement Model VendorProfile
    pass
