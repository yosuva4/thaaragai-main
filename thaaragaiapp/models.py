from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
class Products(models.Model):
    PRODUCT_TYPES = [
        ("Skincare", "Skincare"),
        ("Haircare", "Haircare"),
        ("Oralcare", "Oralcare"),
        ("Footcare", "Footcare"),
        ("Eyecare", "Eyecare"),
        ("Lipcare", "Lipcare"),
        ("Alltype", "Alltype"),
    ]

    PRODUCT_WEIGHT = [
        ("8g", "8 grams"),
        ("10g", "10 grams"),
        ("15g", "15 grams"),
        ("20g", "20 grams"),
        ("25g", "25 grams"),
        ("30g", "30 grams"),
        ("50g", "50 grams"),
        ("60g", "60 grams"),
        ("80g", "80 grams"),
        ("100g", "100 grams"),
        ("120g", "120 grams"),
        ("15ml", "15 milliliters"),
        ("20ml", "20 milliliters"),
        ("25ml", "25 milliliters"),
        ("50ml", "50 milliliters"),
        ("100ml", "100 milliliters"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    productType = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    productName = models.CharField(max_length=40)
    productReview = models.IntegerField()
    oldPrice = models.IntegerField()
    newPrice = models.IntegerField()
    weight = models.CharField(max_length=20, choices=PRODUCT_WEIGHT)
    productBanner = models.ImageField(upload_to="product_banner_images/")
    trendingProduct = models.BooleanField(default=False)
    popularProduct = models.BooleanField(default=False)

    