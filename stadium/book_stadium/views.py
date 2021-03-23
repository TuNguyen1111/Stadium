from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Stadium, StadiumTimeFrame, TimeFrame
# Create your views here.


def get_or_none(model, filter):
    try:
        item = model.objects.get(**filter)
        return item
    except ObjectDoesNotExist:
        return None

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
        if request.user.role != 'owner':
            logout(request)
            return redirect('home')
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        fields = {'fields':fields_by_owner}
        return render(request, 
        'book_stadium/owner.html',
        fields,
        )


class Register(View):
    def post(self, request):
        role = request.POST.get('role')

        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        user = User.objects.create(email=email, role=role, password=password)
        user.save()
        return redirect('home')


class createStadium(LoginRequiredMixin, View):
    login_url = 'home'
    def get(self, request):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        fields = {'fields':fields_by_owner}
        return render(
            request, 
            'book_stadium/createStadium.html',
            fields)

    def post(self,request):
        name = request.POST.get('name')
        address = request.POST.get('address')
        field_count = request.POST.get('field_count')
        owner = request.user
        stadium = Stadium.objects.create(
            name=name, 
            address=address, 
            field_count=field_count,
            owner=owner,
            )
        return redirect('create_stadium')


class StadiumDetail(View):
    def get(self, request, pk):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        current_stadium = Stadium.objects.get(id=pk)
        time_frames = TimeFrame.objects.all()
        prices = []
        for i in time_frames:
            price = get_or_none(StadiumTimeFrame, {'stadium':current_stadium, 'time_frame':i})
            if price:
                price=price.price
            else:
                price = "Not available"
            prices.append(price)
        print(prices)
        stadium_info = {
            'fields':fields_by_owner,
            'stadium': current_stadium,
        }
        return render(
            request,
            'book_stadium/stadiumDetail.html',
            stadium_info,
            )