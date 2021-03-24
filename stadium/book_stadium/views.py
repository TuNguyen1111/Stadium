from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Stadium, StadiumTimeFrame, TimeFrame, Order
from .forms import OrderForm
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

class OwnerPage(LoginRequiredMixin, FormView):
    login_url = "home"
    template_name = "book_stadium/owner.html"
    form_class = OrderForm

    def get(self, request):
        if request.user.role != 'owner':
            logout(request)
            return redirect('home')
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        fields_by_owner2 = Stadium.objects.get(owner=request.user)
        stadium_time_frames = StadiumTimeFrame.objects.filter(stadium=fields_by_owner2)
        total_orders = []
        for order in range(len(stadium_time_frames)):
            owner_order = Order.objects.filter(stadium_time_frame=stadium_time_frames[order])
            if len(owner_order) > 0:
                total_orders.append(owner_order)
        print("Cac san cua chu san la: ", stadium_time_frames)
        fields = {
            'fields': fields_by_owner,
            'total_orders': total_orders,
        }
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


class CreateStadium(LoginRequiredMixin, View):
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
        time_frames = TimeFrame.objects.all()
        for i in time_frames:
            time_frame = StadiumTimeFrame.objects.create(
                stadium=stadium,
                time_frame=i,
                price=300000,
            )
        return redirect('stadium_detail', pk=stadium.id)


class StadiumDetail(LoginRequiredMixin, View):
    login_url = 'home'
    def get(self, request, pk):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        current_stadium = Stadium.objects.get(id=pk)
        times_and_prices = StadiumTimeFrame.objects.filter(stadium=current_stadium)
        page_info = {
            'fields':fields_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
        }
        return render(
            request,
            'book_stadium/stadiumDetail.html',
            page_info,
            )

    def post(self, request, pk):
        name = request.POST.get('name')
        address = request.POST.get('address')
        field_count = request.POST.get('field_count')
        stadium = Stadium.objects.get(id=pk)
        stadium.name = name
        stadium.address = address
        print(stadium.address)
        stadium.field_count = field_count
        stadium.save()
        return redirect('stadium_detail', pk=stadium.id)