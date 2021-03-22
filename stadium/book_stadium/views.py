from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from .models import User
# Create your views here.


class Home(View):
    template_name = 'book_stadium/home.html'
    def get(self, request):
        return render(request, self.template_name)

class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            if user.role == 'owner':
                return redirect('owner')
            return redirect('home')
        else:
            return redirect('home')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class OwnerPage(LoginRequiredMixin, View):
    login_url = "home"
    def get(self, request):
        if request.user.role != "owner":
            logout(request)
            return redirect("home")
        return render(request, 'book_stadium/owner.html')

class Register(View):
    def post(self, request):
        role = request.POST.get('role')

        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        user = User.objects.create(email=email, role=role, password=password)
        user.save()
        return redirect('home')

