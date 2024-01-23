from django.shortcuts import render
from django.views import View 

from django.http import JsonResponse

from .models import Products
class Index(View):
    def get(self, request):

        context = {
            'Products' : Products.objects.all()
        }
        return render(request, 'index.html',context)


class AccountSignin(View):
    def get(self,request):
        return render(request, 'account/signin.html')

class AccountSignup(View):
    def get(self,request):
        return render(request, 'account/signup.html')
    
    def post(self,request):
        first_name = request.POST['first_name']

        print("The First Name is : ",first_name)
        context = {
            'first_name':first_name
        }
        return render(request, 'account/signup.html',context)
    
class AccountForget(View):
    def get(self,request):
        return render(request, 'account/forgot_password.html')