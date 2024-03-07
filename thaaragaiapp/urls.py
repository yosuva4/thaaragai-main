from django.urls import path
from .views import (
    Index,
    AccountSignin,
    AccountSignup,
    AccountForget,
    Filter,
    SingleProduct,
    AccountOrders,
    AddCard,
    AddCard1,
    Favorite,
    FavoriteHtml,
    AccountSignout,
    AccountSettings,
    AccountAddress,
    AccountPayment,
    AccountNotification,
    PlaceOrder,
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("accounts/signin/", AccountSignin.as_view(), name="signin"),
    path("accounts/signout/", AccountSignout.as_view(), name="signout"),
    path("accounts/signup/", AccountSignup.as_view(), name="signup"),
    path("accounts/forget/", AccountForget.as_view(), name="forget"),
    path("product/<productype>/", Filter.as_view(), name="filter"),
    path("singleproduct/<productCode>/", SingleProduct.as_view(), name="singleproduct"),
    path("carts/", AddCard.as_view(), name="cards"),
    path("cards/<id>/", AddCard.as_view(), name="cards"),
    path("cards1/<id>/", AddCard1.as_view(), name="cards"),
    path("favorite/<id>/", Favorite.as_view(), name="favorite"),
    path("favorites/", FavoriteHtml.as_view(), name="favorite"),
    path("myaccount/orders/", AccountOrders.as_view(), name="orders"),
    path("myaccount/settings/", AccountSettings.as_view(), name="settings"),
    path("myaccount/address/", AccountAddress.as_view(), name="address"),
    path("myaccount/payment/", AccountPayment.as_view(), name="payment"),
    path("myaccount/notification/", AccountNotification.as_view(), name="notification"),
    
    path("placeorders/",PlaceOrder.as_view())
]
