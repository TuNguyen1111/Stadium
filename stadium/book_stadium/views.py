from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from .myBackend import CustomBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.forms import inlineformset_factory
from .models import User, Stadium, StadiumTimeFrame, TimeFrame, Order
from .forms import OrderForm, StadiumForm, StadiumTimeFrameForm, UserCreationForm
# Create your views here.

MY_BACKEND = CustomBackend()
class Home(View):
    template_name = 'book_stadium/home.html'
    def get(self, request):
        return render(request, self.template_name)


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = MY_BACKEND.authenticate(username=email, password=password)
        if user:
            login(request, user)
            if user.role == 'owner':
                fields_by_owner = Stadium.objects.filter(owner=request.user)
                if len(fields_by_owner) == 0:
                    return redirect('create_stadium')
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
    template_name = "book_stadium/owner.html"
    
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
        #print("Total order: ", total_orders[0][0].id)
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
    formset = inlineformset_factory(Stadium, StadiumTimeFrame, fields=['time_frame', 'price'], extra=0)
    def get(self, request, pk):
        
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        current_stadium = Stadium.objects.get(id=pk)
        times_and_prices = StadiumTimeFrame.objects.filter(stadium=current_stadium)
        #formset = inlineformset_factory(Stadium, StadiumTimeFrame, fields=['time_frame', 'price'], extra=0)
        formDetail = StadiumForm(instance=current_stadium)
        formTimeFrame = self.formset(instance=current_stadium)
        page_info = {
            'fields':fields_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
            'formDetail': formDetail,
            'formTimeFrame': formTimeFrame
        }
        return render(
            request,
            'book_stadium/stadiumDetail.html',
            page_info,
            )

    def post(self, request, pk):
        formname = request.POST.get('form_type')
        current_stadium = Stadium.objects.get(id=pk)
        stadium = Stadium.objects.get(id=pk)
        if formname == 'form_detail':
            print("AAAAAAAAA")
            formDetail = StadiumForm(request.POST, instance=stadium)
            if formDetail.is_valid():
                formDetail.save()
        else:
            print('SSSSSSSSSSS')
            print("REQUEST", request.POST)
            formTimeFrame = self.formset(request.POST, instance=stadium)
            if formTimeFrame.is_valid():
                formTimeFrame.save()
            else:
                print(formTimeFrame.errors)

        return redirect('stadium_detail', pk=stadium.id)
        


def isAccepted(request, id):
    if request.method == 'POST':
        user = request.POST.get('username_order')
        order = Order.objects.get(id=id)
        order.is_accepted = True
        order.save()
        #print(order)
        return redirect('owner') 
