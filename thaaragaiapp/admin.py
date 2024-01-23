from django.contrib import admin
from .models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ["productType", "productName", "productReview", "oldPrice", "newPrice", "productBanner"]

admin.site.register(Products, ProductsAdmin)
