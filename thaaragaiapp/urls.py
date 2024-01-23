from django.urls import path
from .views import Index, AccountSignin,AccountSignup,AccountForget

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("accounts/signin/", AccountSignin.as_view(), name="signin"),
    path("accounts/signup/", AccountSignup.as_view(), name="signup"),
    path("accounts/forget/", AccountForget.as_view(), name="forget"),
]
