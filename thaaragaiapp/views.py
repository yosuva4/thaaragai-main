from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import JsonResponse
from .models import Products, CustomUser, Cart,Orders

CartsArray = []


def Updates(request):

    if request.user.is_authenticated:
        context = {
            "Carts": Cart.objects.filter(user=request.user),
            "totalCart": sum(
                cart.product_price for cart in Cart.objects.filter(user=request.user)
            ),
            "favorites": len(Products.objects.filter(favorite=True, user=request.user)),
        }
    else:
        totalCart = 0
        for i in request.session["carts__session"]:
            totalCart = totalCart + int(i["product_price"])
        context = {"Carts": request.session["carts__session"], "totalCart": totalCart}

    return context


class Index(View):
    def get(self, request):
        try:
            request.session["carts__session"] = request.session["carts__session"]
        except:
            request.session["carts__session"] = CartsArray

        context = {
            "Products": Products.objects.all(),
        }
        try:
            context.update(Updates(request))
        except Exception as e:
            print("The error is  : ", e)
        return render(request, "index.html", context)


class AccountSignin(View):
    def get(self, request):
        return render(request, "account/signin.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        context = {"username": username, "password": password}

        print(context)

        login_user = authenticate(request, username=username, password=password)

        if login_user is not None:
            for i in request.session["carts__session"]:
                print(i["productCode"])
                product = Products.objects.get(productCode=i["productCode"])
                cart_item, created = Cart.objects.get_or_create(
                    user=login_user, product=product
                )

                if created:
                    cart_item.product_Qty = i["product_Qty"]

                cart_item.product_price = int(cart_item.product_Qty) * int(
                    product.newPrice
                )
                cart_item.save()
            login(request, login_user)
            return redirect("/")
        else:
            context["status"] = True
            print("login failed")
        return render(request, "account/signin.html", context)


class AccountSignout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class AccountSignup(View):
    def get(self, request):
        return render(request, "account/signup.html")

    def post(self, request):
        context = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "password": request.POST["password"],
            "email": request.POST["email"],
        }
        if CustomUser.objects.filter(email=request.POST["email"]).exists():
            context["error"] = "This Email Already Registerd...!"
            return render(request, "account/signup.html", context)
        else:
            user = CustomUser.objects.create_user(
                email=request.POST["email"],
                password=request.POST["password"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
            )
        login(request, user)

        return redirect("/")


class AccountForget(View):
    def get(self, request):
        return render(request, "account/forgot_password.html")


class Filter(View):
    def get(self, request, productype):
        context = {
            "Products": (
                Products.objects.filter(productType=productype)
                if productype != "all"
                else Products.objects.all()
            ),
            "skin_type": productype,
        }
        try:
            context.update(Updates(request))
        except:
            pass

        return render(request, "details/producttype.html", context)


class SingleProduct(View):
    def get(self, request, productCode):
        oneProduct = Products.objects.filter(productCode=productCode)

        productType = ""
        for i in oneProduct:
            productType = i.productType

        ProductTypes = Products.objects.filter(productType=productType)
        context = {
            "Products": oneProduct,
            "ProductTypes": ProductTypes,
        }
        try:
            context.update(Updates(request))
        except:
            pass

        return render(request, "details/single_product.html", context)


# Views.py
class AddCard(View):
    def post(self, request):
        try:
            product_code = request.POST.get("productCode")
            product_qty = int(request.POST.get("productQty"))

            product = Products.objects.get(productCode=product_code)
            user = request.user

            if user.is_authenticated:
                cart_item, created = Cart.objects.get_or_create(
                    user=user, product=product
                )

                if created:
                    cart_item.product_Qty = product_qty
                else:
                    cart_item.product_Qty += product_qty

                cart_item.product_price = int(cart_item.product_Qty) * int(
                    product.newPrice
                )

                cart_item.save()

            else:
                print(request.session["carts__session"])

                data = [
                    True
                    for data in request.session["carts__session"]
                    if data["productCode"] == product_code
                ]
                if data:
                    pass
                else:
                    CartsArray = request.session["carts__session"]
                    CartsArray.append(
                        {
                            "id": product.id,
                            "productBanner": str(product.productBanner.url),
                            "productCode": product_code,
                            "productName": product.productName,
                            "weight": product.weight,
                            "product_Qty": product_qty,
                            "product_price": int(product_qty) * int(product.newPrice),
                        },
                    )
                    request.session["carts__session"] = CartsArray

            return JsonResponse({"message": "Successfully added to the cart"})

        except Products.DoesNotExist:

            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            print("Error in Django View:", str(e))
            return JsonResponse({"error": "Internal Server Error"}, status=500)

    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                Cart.objects.get(id=id).delete()
                return JsonResponse({"message": "Deleted"})
            except:
                return JsonResponse({"message": "Did not deleted "})

        return redirect("/")


class AddCard1(View):
    def get(self, request, id):
        try:
            CartsArray = request.session["carts__session"]
            CartsArray = [C for C in CartsArray if int(C["id"]) != int(id)]
            request.session["carts__session"] = CartsArray
            return JsonResponse({"message": "Deleted"})
        except:
            return JsonResponse({"message": "Did not deleted "})


class Favorite(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                products = Products.objects.get(id=id)
                products.favorite = True
                products.save()
                return JsonResponse({"message": "Added to Favorite"})
            except:
                return JsonResponse({"message": "Did not Added to Favorite "})

        return redirect("/")


class FavoriteHtml(View):
    def get(self, request):
        context = {
            "Products": Products.objects.filter(favorite=True, user=request.user),
        }
        try:
            context.update(Updates(request))
        except:
            pass

        return render(request, "myaccount/favorites.html", context)


class AccountOrders(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                "Orders": Orders.objects.filter(user=request.user),
            }
            context.update(Updates(request))
            return render(request, "myaccount/orders.html", Updates(request))
        else:
            return redirect("/accounts/signin/")


class AccountSettings(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                "Orders": Products.objects.filter(user=request.user),
            }
            context.update(Updates(request))
            return render(request, "myaccount/settings.html", context)
        else:
            return redirect("/accounts/signin/")


class AccountAddress(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "myaccount/address.html", Updates(request))
        else:
            return redirect("/accounts/signin/")
        
    def post(self,request):
        if request.user.is_authenticated:
            return render(request, "myaccount/address.html", Updates(request)) 
        
        else:
            return redirect("/accounts/signin/")



class AccountPayment(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "myaccount/payment.html", Updates(request))
        else:
            return redirect("/accounts/signin/")


class AccountNotification(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "myaccount/notification.html", Updates(request))
        else:
            return redirect("/accounts/signin/")
