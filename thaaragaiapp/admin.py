from django.contrib import admin
from .models import Products,CustomUser,Cart

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('productName', 'productReview', 'oldPrice', 'newPrice', 'weight', 'trendingProduct', 'popularProduct')

    

admin.site.register(Products, ProductsAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "is_active"]

admin.site.register(CustomUser, CustomUserAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Cart, CartAdmin)


