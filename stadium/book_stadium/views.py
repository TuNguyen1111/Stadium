from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponse, redirect, render
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime
import datetime

from .forms import (OrderForm, StadiumForm, StadiumTimeFrameForm,
                    UserCreationForm, UserProfileForm)
from .models import Order, Stadium, StadiumTimeFrame, TimeFrame, User
from .myBackend import CustomBackend

# Create your views here.

MY_BACKEND = CustomBackend()

# def checkRoleOfUser(request, user):
#     if user.role == "owner":
#         fields_by_owner = Stadium.objects.filter(owner=request.user)
#         if len(fields_by_owner) == 0:
#             return redirect('create_stadium')
#         return redirect('owner')
#     else:
#         if user.username == 'User' or user.phone_number == None:
#             return redirect('user_profile', user.id)
#         return redirect('home')
class Home(View):
    form_class = UserCreationForm
    template_name = 'book_stadium/home.html'
    #fields_by_owner = Stadium.objects.filter(owner=request.user)
    def get(self, request):
        context = {
            'register_form' : self.form_class,
        }
        return render(
            request,
            self.template_name,
            context
            )

class Register(View):
    # t đã chỉnh username field của bảng user thành id rồi để đảm bảo nó duy nhất nên là phone_number với email có thể ko có cũng đc nha.
    form_class = UserCreationForm

    def post(self, request):
        create_user_form = self.form_class(request.POST)
        if create_user_form.is_valid():
            user = create_user_form.save()
            login(request, user, backend='book_stadium.myBackend.CustomBackend')
            #checkRoleOfUser(request, user)
            if user.role == "owner":
                return redirect('create_stadium')

            else:
                if user.username == '' or user.phone_number == '':
                    return redirect('user_profile', user.id)
                return redirect('home')
        else:
            # sửa đẩy form.errors về html nha
            context = {
                'register_form': create_user_form
            }
            print(create_user_form.errors)
            return render(request, 'book_stadium/home.html', context)
        return redirect('home')


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = MY_BACKEND.authenticate(request, username=email, password=password)
        if user:
            login(request, user, backend='book_stadium.myBackend.CustomBackend')
            #checkRoleOfUser(request, user)
            if user.role == 'owner':
                stadiums = Stadium.objects.filter(owner=request.user)

                if len(stadiums) == 0:
                    return redirect('create_stadium')
                else:
                    fisrt_stadium = stadiums.first()
                    return redirect('owner', fisrt_stadium.id)
            else:
                if user.username == '' or user.phone_number == '':
                    return redirect('user_profile', user.id)
        else:
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu không đúng! Thử lại hộ cái bạn êiiiiii')
        return redirect('home')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class OwnerPage(LoginRequiredMixin, View):
    login_url = "home"
    template_name = "book_stadium/owner.html"

    def get(self, request, id):
        if request.user.role != 'owner':
            logout(request)
            return redirect('home')
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        stadium = Stadium.objects.get(id=id)
        all_time_frames = TimeFrame.objects.all()
        today = timezone.now()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        orders = Order.objects.filter(stadium_time_frame__stadium=stadium, order_date__gte=timezone.now())\
                              .order_by('order_date')
        is_today_in_all_orders = False
        all_orders = []
        for order in orders:
            if today.date().strftime('%Y/%m/%d') == order.order_date.strftime('%Y/%m/%d'):
                is_today_in_all_orders = True

        #tao 1 dict rong neu nhu ngay hien tai khong co order nao
        if not is_today_in_all_orders:
            first_order = {
                'ngay': 'Hôm nay' ,
                'khung_gio': {}
            }
            all_orders.append(first_order)
            time_frames = all_orders[0]['khung_gio']
            for time_frame in all_time_frames:
                time = str(time_frame)
                is_same_timeframe = time in time_frames
                if is_same_timeframe:
                    current_timeframe = time_frames[time]
                else:
                    current_timeframe = {
                        'con_trong': None,
                        'nguoi_dat': []
                    }
                    time_frames[time] = current_timeframe

        #tao dict voi moi ngay co order
        for order in orders:
            is_same_day = False
            if all_orders:
                #lay ra order cuoi va check xem co cung ngay hay khong
                last_order = all_orders[-1]
                is_same_day = last_order['ngay'] == order.order_date.strftime('%Y/%m/%d')
            if is_same_day:
                current_order = all_orders[-1]
            else:
                current_order = {
                    'ngay': order.order_date.strftime('%Y/%m/%d'),
                    'khung_gio': {}
                }
                if order.order_date == today.date():
                    current_order['ngay'] = 'Hôm nay'
                if order.order_date == tomorrow:
                    current_order['ngay'] = 'Ngày mai'
                all_orders.append(current_order)

            time_frames = current_order['khung_gio']
            for time_frame in all_time_frames:
                time = str(time_frame)
                is_same_timeframe = time in time_frames
                if is_same_timeframe:
                    current_timeframe = time_frames[time]
                else:
                    current_timeframe = {
                        'con_trong': None,
                        'nguoi_dat': []
                    }
                    time_frames[time] = current_timeframe
                if time == str(order.stadium_time_frame.time_frame):
                    customer = {
                        'sdt': order.user.phone_number,
                        'ten': order.user.username,
                        'da_duyet': order.is_accepted,
                        'order_id': order.id
                    }
                    current_timeframe['nguoi_dat'].append(customer)

        #dem xem khung gio con bao nhieu san trong dua tren so nguoi da duyet
        for order in all_orders:
            for key, time_frame in order['khung_gio'].items():
                count_accept_user = 0
                for user in time_frame['nguoi_dat']:
                    if user['da_duyet']:
                        count_accept_user += 1
                total_stadium = stadium.field_count - count_accept_user
                time_frame['con_trong'] = total_stadium
        import json
        print(json.dumps(all_orders, indent=4))
        print(datetime.date.today() + datetime.timedelta(days=1))
        fields = {

            'fields': fields_by_owner,
            'all_orders': all_orders
        }
        return render(request,
            'book_stadium/owner.html',
            fields,
        )

def isAccepted(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        form_type = request.POST.get('form_type')
        print('form', form_type)

        stadium = order.stadium_time_frame.stadium
        if form_type == "accept-input":
            order.is_accepted = True
            order.save()
            messages.success(request, 'Đã duyệt!')
        elif form_type == "accept-delete":
            order.delete()
            messages.success(request, 'Xóa thành công!')
        return redirect('owner', stadium.id)

class CreateStadium(LoginRequiredMixin, View):
    login_url = 'home'
    create_stadium_form = StadiumForm

    def get(self, request):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        form = self.create_stadium_form
        context = {
            'fields':fields_by_owner,
            'form':form
            }
        return render(
            request,
            'book_stadium/createStadium.html',
            context)

    def post(self,request):
        create_stadium_form = self.create_stadium_form(request.POST, request.FILES)
        owner = request.user
        if create_stadium_form.is_valid():
            # nếu form valid thì đẩy owner bằng request.user rồi mới save nha
            instance = create_stadium_form.save(commit=False)
            instance.owner = owner
            instance.save()
        else:
            # tương tự, nhớ đẩy error về cho HTML
            print(create_stadium_form.errors)
        stadium = Stadium.objects.get(name=request.POST.get("name"))
        time_frames = TimeFrame.objects.all()
        for i in time_frames:
            time_frame = StadiumTimeFrame.objects.create(
                stadium=stadium,
                time_frame=i,
                price=300000,
            )
        messages.info(request, 'Tạo sân thành công!')
        return redirect('stadium_detail', pk=stadium.id)


class StadiumDetail(LoginRequiredMixin, View):
    login_url = 'home'
    formset = inlineformset_factory(Stadium, StadiumTimeFrame, form=StadiumTimeFrameForm, extra=0)

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
        owner = request.user
        if formname == 'form_detail':
            form_detail = StadiumForm(request.POST, request.FILES, instance=stadium)
            if form_detail.is_valid():
                # như trên, đẩy owner vào.
                instance = form_detail.save(commit=False)
                instance.owner = owner
                instance.save()
            else:
                print(form_detail.errors)
        else:
            formTimeFrame = self.formset(request.POST, instance=stadium)
            if formTimeFrame.is_valid():
                formTimeFrame.save()
            else:
                print(formTimeFrame.errors)
        messages.success(request, 'Cập nhật thành công!')
        return redirect('stadium_detail', pk=stadium.id)


class UserProfile(View):
    form_class = UserProfileForm

    def get(self, request, id):
        user = User.objects.get(id=id)
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        form = self.form_class(instance=user)
        context = {
            'form': form,
            'fields':fields_by_owner,
        }
        return render(request, 'book_stadium/userProfile.html', context)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect('home')


class BookStadium(ListView):

    def get(self, request):
        stadium_timeframes = StadiumTimeFrame.objects.all().order_by('time_frame__start_time')
        current_day = datetime.date.today() + datetime.timedelta(days=0)
        all_stadiums = []


        for number in range(8):
            current_day = datetime.date.today() + datetime.timedelta(days=number)
            timeframe_fixed = '6:30:00 - 17:00:00'
            day = {
                'ngay': current_day.strftime('%Y/%m/%d'),
                'khung_gio': {}
            }
            all_stadiums.append(day)

            stadium = all_stadiums[-1]
            timeframes_of_day = stadium['khung_gio']
            is_have_6_to_17_in_dict = timeframe_fixed in timeframes_of_day
            if not is_have_6_to_17_in_dict:
                timeframes_of_day[timeframe_fixed] = []

            for timeframe in stadium_timeframes:
                orders = Order.objects.filter(stadium_time_frame=timeframe)
                is_in_6_to_17 = (
                    timeframe.time_frame.start_time >= datetime.time(6) and
                    timeframe.time_frame.end_time <= datetime.time(17)
                )
                stadium_of_timeframe = timeframe.stadium

                if orders:
                    count_order_accepted = 0
                    for order in orders:
                        if order.order_date == current_day and order.is_accepted:
                            count_order_accepted += 1
                    if count_order_accepted < stadium_of_timeframe.field_count:
                        if is_in_6_to_17:
                            current_timeframe = timeframes_of_day[timeframe_fixed]
                        else:
                            time = str(timeframe.time_frame)
                            current_timeframe = []
                            timeframes_of_day[time] = current_timeframe
                        self.check_is_same_stadium(current_timeframe, stadium_of_timeframe)
                else:
                    if is_in_6_to_17:
                        current_timeframe = timeframes_of_day[timeframe_fixed]
                    else:
                        time = str(timeframe.time_frame)
                        is_same_timeframe = time in timeframes_of_day

                        if is_same_timeframe:
                            current_timeframe = timeframes_of_day[time]
                        else:
                            current_timeframe = []
                            timeframes_of_day[time] = current_timeframe
                    self.check_is_same_stadium(current_timeframe, stadium_of_timeframe)

        paginator = Paginator(all_stadiums, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # import json
        # print(json.dumps(all_stadiums, indent=4))
        print(page_number)
        context = {
            'stadiums': all_stadiums,
            'page_obj': page_obj
        }
        return render(request, 'book_stadium/book_stadium.html', context)

    def check_is_same_stadium(self, current_timeframe, stadium_of_timeframe):
        stadiums = []
        for single_stadium in current_timeframe:
            stadium_id = single_stadium['id']
            stadiums.append(stadium_id)
        is_same_stadium = stadium_of_timeframe.id in stadiums
        if not is_same_stadium:
            stadium_detail = {
                'anh': stadium_of_timeframe.image.url,
                'ten': stadium_of_timeframe.name,
                'dia_chi': stadium_of_timeframe.address,
                'id': stadium_of_timeframe.id
            }
            current_timeframe.append(stadium_detail)




# all_orders = [
        #     {
        #         'ngay': '22/2/2020',
        #         'khung_gio': {
        #             '6h': {
        #                 'con_trong': 4,
        #                 'nguoi_dat':[
        #                     {
        #                         'sdt': '0912321312',
        #                         'ten': 'ong',
        #                         'da_duyet': False
        #                     },
        #                     {
        #                         'sdt': '01211231',
        #                         'ten': 's',
        #                         'da_duyet': False
        #                     },
        #                 ]
        #             },
        #             '8h30': {
        #                 'con_trong': 3,
        #                 'nguoi_dat': [
        #                     {
        #                         'sdt': '23423423',
        #                         'ten': '2aaaaa',
        #                         'da_duyet': False
        #                     },
        #                     {
        #                         'sdt': '0876756',
        #                         'ten': 'dd',
        #                         'da_duyet': False
        #                     },
        #                 ]
        #             },
        #         }
        #     },
        #     {
        #         'ngay': '23/2/2020',
        #         'khung_gio': {
        #         '6h': {
        #             'con_trong': 3,
        #             'nguoi_dat':[
        #                 {
        #                     'sdt': '0763743',
        #                     'ten': 'ong2',
        #                     'da_duyet': False
        #                 },
        #                 {
        #                     'sdt': '04545454',
        #                     'ten': 's2',
        #                     'da_duyet': False
        #                 },
        #             ]
        #         },
        #         '8h30': {
        #             'con_trong': 3,
        #             'nguoi_dat': [
        #                 {
        #                     'sdt': '0121212',
        #                     'ten': 'ba',
        #                     'da_duyet': False
        #                 },
        #                 {
        #                     'sdt': '04456456',
        #                     'ten': 'da',
        #                     'da_duyet': False
        #                 },
        #             ]
        #         },
        #         }
        #     },
        # ]
# for index, stadium in enumerate(all_stadiums):
        #     current_day_timeframe = stadium['khung_gio']
        #     if index == 0:
        #         current_day = timezone.now().date()
        #     else:
        #         current_day = datetime.date.today() + datetime.timedelta(days=1)

        #     for timeframe in stadium_timeframes:
        #         orders = Order.objects.filter(stadium_time_frame=timeframe)
        #         # is_in_6_17 = timeframe.time_frame.end_time.strftime('%H:%M:%S') in time_frame_from_6h_17h

        #         is_in_6_17 = (
        #             timeframe.time_frame.start_time >= datetime.time(6) and
        #             timeframe.time_frame.end_time <= datetime.time(17)
        #         )

        #         stadium_of_timeframe = timeframe.stadium

        #         if orders:
        #             count_order_accepted = 0
        #             for order in orders:
        #                 if order.order_date == current_day and order.is_accepted:
        #                     count_order_accepted += 1
        #             if count_order_accepted < stadium_of_timeframe.field_count:
        #
        #                 if is_in_6_17:
        #                     current_timeframe = current_day_timeframe['06:30:00-17:00:00']
        #                 else:
        #                     current_timeframe = []
        #                     time = str(timeframe.time_frame)
        #                     current_day_timeframe[time] = current_timeframe
        #                 self.check_is_same_name(stadiums, current_timeframe, stadium_of_timeframe)
        #         else:
        #
        #             if is_in_6_17:
        #                 current_timeframe = current_day_timeframe['06:30:00-17:00:00']
        #                 self.check_is_same_name(stadium_names, current_timeframe, stadium_of_timeframe)

        #             else:
        #                 is_same_timeframe = str(timeframe.time_frame) in current_day_timeframe
        #                 time = str(timeframe.time_frame)

        #                 if is_same_timeframe:
        #                     current_timeframe = current_day_timeframe[time]
        #                 else:
        #                     current_timeframe = []
        #                     current_day_timeframe[time] = current_timeframe
        #                 self.check_is_same_name(stadium_names, current_timeframe, stadium_of_timeframe)
