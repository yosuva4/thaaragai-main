from django.db import models
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
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

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Products(models.Model):
    PRODUCT_TYPES = (
        ("Skincare", "Skincare"),
        ("Haircare", "Haircare"),
        ("Oralcare", "Oralcare"),
    )

    P_TYPES = (
        ("Gel ", "Gel "),
        ("Oil", "Oil"),
    )

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

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="products"
    )

    productType = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    productCode = models.CharField(max_length=10, unique=True)
    productName = models.CharField(max_length=40)
    productBrand = models.CharField(max_length=40)

    productReview = models.IntegerField()
    packageQty = models.IntegerField()

    oldPrice = models.IntegerField()
    newPrice = models.IntegerField()
    weight = models.CharField(max_length=20, choices=PRODUCT_WEIGHT)

    p_type = models.CharField(max_length=20, choices=P_TYPES)

    trendingProduct = models.BooleanField(default=False)
    popularProduct = models.BooleanField(default=False)
    avalability = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    productBanner = models.ImageField(upload_to="product_banner_images/")
    productImg1 = models.ImageField(upload_to="product_images/")
    productImg2 = models.ImageField(upload_to="product_images/")
    productImg3 = models.ImageField(upload_to="product_images/")

    description = RichTextUploadingField(max_length=10000)
    benifits = RichTextUploadingField(max_length=10000)
    keyIngredients = RichTextUploadingField(max_length=10000)
    howToUse = RichTextUploadingField(max_length=10000)

    def __str__(self):
        return self.productCode

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_Qty = models.IntegerField(default=0, null=False, blank=False)
    product_price = models.IntegerField(default=0, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_Qty = models.IntegerField(default=0, null=False, blank=False)
    total_amt = models.IntegerField(default=0, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class CustomerAddress(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)