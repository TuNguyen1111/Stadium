# REVIEW:
# 1. Bỏ các import không dùng. VD: HttpResponse, make_password
# 2. Tách view ra thành nhiều file. VD:
# |_ views
# |__ __init__.py
# |__ home.py
# |__ register.py
# v.v.
# Trong file __init__.py sẽ import các view:
# from .home import Home
# from .register import Register

from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime

from notifications.signals import notify
from swapper import load_model

import datetime

from .forms import (OrderForm, StadiumForm, StadiumTimeFrameForm, StadiumFormForUser,
                    UserCreationForm, UserProfileForm, ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form, CommentForm)
from .models import Order, Stadium, StadiumTimeFrame, TimeFrame, User, Comment, Roles
from .myBackend import CustomAuthenticatedBackend

import json
# Create your views here.

CustomAuthenticatedBackend = CustomAuthenticatedBackend()

Notification = load_model('notifications', 'Notification')


class Home(View):
    form_class = UserCreationForm
    template_name = 'book_stadium/home.html'
    # fields_by_owner = Stadium.objects.filter(owner=request.user)

    def get(self, request):
        context = {
            'register_form': self.form_class,
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
            login(request, user,
                  backend='book_stadium.myBackend.CustomAuthenticatedBackend')
            # checkRoleOfUser(request, user)

            if user.role == Roles.OWNER:
                return redirect('create_stadium')

            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
                return redirect('home')
        else:
            # sửa đẩy form.errors về html nha
            context = {
                'register_form': create_user_form
            }
            return render(request, 'book_stadium/home.html', context)


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomAuthenticatedBackend.authenticate(
            request, username=email, password=password)

        if user:
            login(request, user,
                  backend='book_stadium.myBackend.CustomAuthenticatedBackend')
            # checkRoleOfUser(request, user)
            if user.role == Roles.OWNER:
                stadiums = Stadium.objects.filter(owner=request.user)

                if len(stadiums) == 0:
                    return redirect('create_stadium')
                else:
                    fisrt_stadium = stadiums.first()
                    return redirect('owner', fisrt_stadium.pk)
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
        return redirect('home')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class OwnerPage(LoginRequiredMixin, UserPassesTestMixin, View):
    # login_url = "home"
    template_name = 'book_stadium/owner.html'

    def get(self, request, pk):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        stadium = Stadium.objects.get(pk=pk)
        all_time_frames = TimeFrame.objects.all()
        today = timezone.now()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        orders = Order.objects.filter(stadium_time_frame__stadium=stadium, order_date__gte=timezone.now())\
                              .order_by('order_date')
        all_orders = []
        update_stadium_7players_form = ChangeNumberOfStadium7Form()
        update_stadium_11players_form = ChangeNumberOfStadium11Form()

        self.general_orders(all_orders, orders, stadium)
        # tao dict voi moi ngay co order
        for order in orders:
            is_same_day = False
            if all_orders:
                # lay ra order cuoi va check xem co cung ngay hay khong
                last_order = all_orders[-1]
                if last_order['ngay'] == 'Hôm nay':
                    last_order['ngay'] = today.date().strftime('%Y/%m/%d')
                elif last_order['ngay'] == 'Ngày mai':
                    last_order['ngay'] = tomorrow.strftime('%Y/%m/%d')

                is_same_day = last_order['ngay'] == order.order_date.strftime(
                    '%Y/%m/%d')
                print(is_same_day, last_order['ngay'],
                      order.order_date.strftime('%Y/%m/%d'))
            if is_same_day:
                current_order = all_orders[-1]
            else:
                current_order = {
                    'ngay': order.order_date.strftime('%Y/%m/%d'),
                    'khung_gio': {}
                }
                if order.order_date == today.date():
                    current_order['ngay'] = 'Hôm nay'
                elif order.order_date == tomorrow:
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
                        'sdt': order.customer_phone_number,
                        'ten': order.customer_name,
                        'da_duyet': order.is_accepted,
                        'order_id': order.pk,
                        # 'vi_tri': order.field_numbers,
                        'ao_tap': order.pitch_clothes,
                        'loai_san': order.type_stadium,
                        'tong_san': stadium.field_count
                    }

                    if order.type_stadium == "7players":
                        customer['vi_tri'] = order.field_numbers
                    else:
                        if order.is_accepted:
                            three_field = ""
                            for field in order.field_numbers:
                                three_field += f'{field} '
                            customer['vi_tri'] = three_field
                        else:
                            customer['vi_tri'] = order.field_numbers

                    current_timeframe['nguoi_dat'].append(customer)
        # dem xem khung gio con bao nhieu san trong dua tren so nguoi da duyet
        for order in all_orders:
            for key, time_frame in order['khung_gio'].items():
                count_accept_user = 0
                for user in time_frame['nguoi_dat']:
                    if user['da_duyet']:
                        if user['loai_san'] == "7players":
                            count_accept_user += 1
                        else:
                            count_accept_user += 3
                total_stadium = stadium.field_count - count_accept_user
                time_frame['con_trong'] = total_stadium
        # import json
        # print(json.dumps(all_orders, indent=4))
        fields = {

            'fields': fields_by_owner,
            'all_orders': all_orders,
            'update_stadium_7players_form': update_stadium_7players_form,
            'update_stadium_11players_form': update_stadium_11players_form
        }
        return render(request,
                      'book_stadium/owner.html',
                      fields,
                      )

    def general_orders(self, all_orders, orders, stadium):
        all_time_frames = TimeFrame.objects.all()
        today = timezone.now()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        is_today_in_all_orders = False

        for order in orders:
            if today.date().strftime('%Y/%m/%d') == order.order_date.strftime('%Y/%m/%d'):
                is_today_in_all_orders = True

        if not is_today_in_all_orders:
            first_order = {
                'ngay': 'Hôm nay',
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

    def test_func(self):
        return self.request.user.role == Roles.OWNER

    def handle_no_permission(self):
        return HttpResponse('You have been denied')


class CreateStadium(LoginRequiredMixin, View):
    login_url = 'home'
    create_stadium_form = StadiumForm

    def get(self, request):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        form = self.create_stadium_form

        context = {
            'fields': fields_by_owner,
            'form': form
        }
        return render(
            request,
            'book_stadium/createStadium.html',
            context)

    def post(self, request):
        create_stadium_form = self.create_stadium_form(
            request.POST, request.FILES)
        owner = request.user

        if create_stadium_form.is_valid():
            # nếu form valid thì đẩy owner bằng request.user rồi mới save nha
            instance = create_stadium_form.save(commit=False)
            instance.owner = owner
            instance.save()

        stadium = Stadium.objects.get(name=request.POST.get("name"))
        time_frames = TimeFrame.objects.all()

        for i in time_frames:
            time_frame = StadiumTimeFrame.objects.create(
                stadium=stadium,
                time_frame=i,
                price=300000,
            )
        messages.success(request, 'Tạo sân thành công!')
        return redirect('stadium_detail', pk=stadium.pk)


class StadiumDetail(LoginRequiredMixin, View):
    login_url = 'home'
    formset = inlineformset_factory(
        Stadium, StadiumTimeFrame, form=StadiumTimeFrameForm, extra=0)

    def get(self, request, pk):
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        current_stadium = Stadium.objects.get(pk=pk)
        times_and_prices = StadiumTimeFrame.objects.filter(
            stadium=current_stadium)
        formDetail = StadiumForm(instance=current_stadium)
        formTimeFrame = self.formset(instance=current_stadium)
        form_detail_for_user = StadiumFormForUser(instance=current_stadium)
        comments_of_stadium = Comment.objects.filter(stadium=current_stadium)
        comment_form = CommentForm()

        page_info = {
            'fields': fields_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
            'formDetail': formDetail,
            'formTimeFrame': formTimeFrame,
            'form_detail_for_user': form_detail_for_user,
            'comments_of_stadium': comments_of_stadium,
            'comment_form': comment_form
        }
        return render(
            request,
            'book_stadium/stadiumDetail.html',
            page_info,
        )

    def post(self, request, pk):
        formname = request.POST.get('form_type')
        stadium = Stadium.objects.get(pk=pk)
        owner = request.user

        if formname == 'form_detail':
            form_detail = StadiumForm(
                request.POST, request.FILES, instance=stadium)

            if form_detail.is_valid():
                # như trên, đẩy owner vào.
                instance = form_detail.save(commit=False)
                instance.owner = owner
                instance.save()
            else:
                print(form_detail.errors)

        elif formname == 'form_time':
            formTimeFrame = self.formset(request.POST, instance=stadium)

            if formTimeFrame.is_valid():
                formTimeFrame.save()

        elif formname == 'delete-input':
            stadium.delete()
            return redirect('book_stadium')

        messages.success(request, 'Cập nhật thành công!')
        return redirect('stadium_detail', pk=stadium.pk)


class StadiumRating(View):
    def post(self, request):
        if request.is_ajax():
            star_point = int(request.POST.get('starPoint'))
            comment = request.POST.get('commentData')
            stadium_id = int(request.POST.get('stadiumId'))
            stadium = Stadium.objects.get(pk=stadium_id)

            new_comment = Comment.objects.create(
                user=request.user, stadium=stadium, comment=comment, star_point=star_point)
            new_comment.save()

            data_respone = {
                'username': request.user.username,
                'comment': new_comment.comment,
                'star_point': new_comment.star_point
            }
            return JsonResponse({'data_respone': data_respone})


class UserProfile(View):
    form_class = UserProfileForm

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        form = self.form_class(instance=user)

        context = {
            'form': form,
            'fields': fields_by_owner,
        }
        return render(request, 'book_stadium/userProfile.html', context)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=user)

        if form.is_valid():
            form.save()

        messages.success(request, 'Cập nhật thông tin thành công!')
        return redirect('user_profile', user.pk)


class BookStadium(ListView):
    form_class = OrderForm

    def get(self, request):
        register_form = UserCreationForm
        order_form = self.form_class
        stadium_timeframes = StadiumTimeFrame.objects.filter(
            is_open=True).order_by('time_frame__start_time')
        all_stadiums = []
        self.put_out_null_stadiums_and_timesframe(
            all_stadiums, stadium_timeframes)
        paginator = Paginator(all_stadiums, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        day_search = request.GET.get('day-search')
        time_frame_search = request.GET.get('time_frame')
        address_search = request.GET.get('address-search')
        stadium_name_search = request.GET.get('stadium-name-search')

        stadium_search_result = self.search_stadium(day_search, time_frame_search,
                                                    address_search, stadium_name_search)

        if request.user.is_authenticated:
            fields_by_owner = Stadium.objects.filter(owner=request.user)
        else:
            fields_by_owner = ''
        # print(json.dumps(all_stadiums, indent=4))

        context = {
            'fields': fields_by_owner,
            'stadiums': all_stadiums,
            'page_obj': page_obj,
            'order_form': order_form,
            'stadium_search_result': stadium_search_result,
            'register_form': register_form,
        }
        return render(request, 'book_stadium/book_stadium.html', context)

    def post(self, request):
        order_form = self.form_class(request.POST)

        if order_form.is_valid():
            order = order_form.save()
            stadium_name_notification = order.stadium_time_frame.stadium.name
            timeframe_notification = order.stadium_time_frame.time_frame
            date_notification = order.order_date
            receiver = order.stadium_time_frame.stadium.owner
            sender_name = order.customer_name
            user = request.user

            if user.is_authenticated:
                order.user = user
                order.save()
                sender = request.user
            else:
                pass
                # sender = User.objects.get(pk=10)

            notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender_name}',
                        description=f'{sender_name} đã đặt sân {stadium_name_notification} của bạn vào ngày {date_notification}, khung giờ {timeframe_notification}')
            messages.success(request, 'Đặt sân thành công!')

        else:
            messages.warning(request, 'Vui long chon khung gio khac!')

        return redirect('book_stadium')

    def put_out_null_stadiums_and_timesframe(self, all_stadiums, stadium_timeframes):
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
            count_stadium_in_timeframe_6_to_17 = 4
            count_stadium_in_timeframe = 4
            total_stadium_in_6_to_17 = len(timeframes_of_day[timeframe_fixed])

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
                        self.check_is_same_stadium(
                            current_timeframe, stadium_of_timeframe, timeframe)
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
                    self.check_is_same_stadium(
                        current_timeframe, stadium_of_timeframe, timeframe)

    def check_is_same_stadium(self, current_timeframe, stadium_of_timeframe, timeframe):
        if len(current_timeframe) < 4:
            stadiums = []

            for single_stadium in current_timeframe:
                stadium_id = single_stadium['id']
                stadiums.append(stadium_id)
            is_same_stadium = stadium_of_timeframe.pk in stadiums

            if not is_same_stadium:
                stadium_detail = {
                    'anh': stadium_of_timeframe.image.url,
                    'ten': stadium_of_timeframe.name,
                    'dia_chi': stadium_of_timeframe.address,
                    'sdt': stadium_of_timeframe.owner.phone_number,
                    'id': stadium_of_timeframe.pk,
                    'khung_gio_dat': timeframe.time_frame.pk
                }
                current_timeframe.append(stadium_detail)

    def search_stadium(self, day_search, time_frame_search, address_search, stadium_name_search):
        stadium_search_result = []

        if day_search:
            day_search = day_search.replace('/', '-')
            if not stadium_name_search:
                stadiums_timeframe_search = StadiumTimeFrame.objects.filter(
                    time_frame=time_frame_search, stadium__address=address_search)

            elif not address_search:
                stadiums_timeframe_search = StadiumTimeFrame.objects.filter(
                    time_frame=time_frame_search, stadium__name=stadium_name_search)

            elif stadium_name_search and address_search:
                stadiums_timeframe_search = StadiumTimeFrame.objects.filter(
                    time_frame=time_frame_search, stadium__name=stadium_name_search, stadium__address=address_search)

            for timeframe in stadiums_timeframe_search:
                orders = Order.objects.filter(
                    stadium_time_frame=timeframe, order_date=day_search)
                stadium_of_timeframe = timeframe.stadium

                if orders:
                    count_order_accepted = 0

                    for order in orders:
                        if order.is_accepted:
                            count_order_accepted += 1

                    if count_order_accepted < stadium_of_timeframe.field_count:
                        self.add_stadium_obj(
                            stadium_search_result, day_search, stadium_of_timeframe, timeframe)
                else:
                    self.add_stadium_obj(
                        stadium_search_result, day_search, stadium_of_timeframe, timeframe)

        return stadium_search_result

    def add_stadium_obj(self, stadium_search_result, day_search, stadium_of_timeframe, timeframe):
        if stadium_search_result:
            search_obj = stadium_search_result[-1]
        else:
            search_obj = {}
            search_obj['ngay'] = day_search
            timeframe_obj = {}
            search_obj['khung_gio'] = timeframe_obj
            all_stadiums_obj = []
            time = str(timeframe.time_frame)
            timeframe_obj[time] = all_stadiums_obj
            stadium_search_result.append(search_obj)

        stadium_obj = {}
        stadium_obj['anh'] = stadium_of_timeframe.image.url
        stadium_obj['ten'] = stadium_of_timeframe.name
        stadium_obj['dia_Chi'] = stadium_of_timeframe.address
        stadium_obj['sdt'] = stadium_of_timeframe.owner.phone_number
        stadium_obj['id'] = stadium_of_timeframe.pk
        search_obj['khung_gio'][time].append(stadium_obj)

        return stadium_search_result


class HistoryBookedOfUser(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user_orders = Order.objects.filter(user=user)

        all_orders_of_user = []
        start_day = request.GET.get('start-day')
        end_day = request.GET.get('end-day')

        conditions = {}

        if start_day:
            start_day = start_day.replace('/', '-')
            conditions['order_date__gte'] = start_day
        if end_day:
            end_day = end_day.replace('/', '-')
            conditions['order_date__lte'] = end_day

        user_orders = user_orders.filter(**conditions).order_by('order_date')

        self.general_order_of_user(user_orders, all_orders_of_user)

        context = {
            'all_orders_of_user': all_orders_of_user
        }
        return render(request, 'book_stadium/historyBookedOfUser.html', context)

    def post(self, request, pk):
        user = request.user
        order = Order.objects.get(pk=pk)
        order.delete()
        return redirect('history_booked', user.pk)

    def general_order_of_user(self,  user_orders, all_orders_of_user):
        for order in user_orders:
            is_same_day = False
            if all_orders_of_user:
                last_order = all_orders_of_user[-1]
                is_same_day = last_order['ngay'] == order.order_date.strftime(
                    '%Y/%m/%d')
            if is_same_day:
                current_order = all_orders_of_user[-1]
            else:
                current_order = {
                    'ngay':  order.order_date.strftime('%Y/%m/%d'),
                    'khung_gio': {}
                }
                all_orders_of_user.append(current_order)

            timeframe_of_order = order.stadium_time_frame.time_frame
            stadium_of_timeframe = order.stadium_time_frame.stadium
            time = str(timeframe_of_order)
            timeframes = current_order['khung_gio']
            is_same_timeframe = time in timeframes
            if is_same_timeframe:
                current_timeframe = timeframes[time]
            else:
                current_timeframe = []
                timeframes[time] = current_timeframe
            stadium_obj = {
                'san': stadium_of_timeframe.name,
                'trang_thai': order.is_accepted,
                'order_id': order.pk
            }
            current_timeframe.append(stadium_obj)


class SearchStadium(BookStadium):
    def get(self, request):
        order_form = self.form_class
        user = request.user

        all_stadiums = Stadium.objects.all()
        stadium_search_result = []

        paginator = Paginator(all_stadiums, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        day_search = request.GET.get('day-search')
        time_frame_search = request.GET.get('time_frame')
        address_search = request.GET.get('address-search')
        stadium_name_search = request.GET.get('stadium-name-search')

        self.search_stadium(stadium_search_result, day_search,
                            time_frame_search, address_search, stadium_name_search)

        # import json
        # # print(json.dumps(all_stadiums, indent=4))

        context = {
            # 'fields': fields_by_owner,
            'stadiums': all_stadiums,
            'page_obj': page_obj,
            'order_form': order_form,
            'stadium_search_result': stadium_search_result,

        }

        if user.is_authenticated:
            fields_by_owner = Stadium.objects.filter(owner=user)
            context['fields'] = fields_by_owner
        return render(request, 'book_stadium/searchStadium.html', context)

    def check_is_same_stadium(self, current_timeframe, stadium_of_timeframe, timeframe):
        stadiums = []
        for single_stadium in current_timeframe:
            stadium_id = single_stadium['id']
            stadiums.append(stadium_id)
        is_same_stadium = stadium_of_timeframe.pk in stadiums
        if not is_same_stadium:
            stadium_detail = {
                'anh': stadium_of_timeframe.image.url,
                'ten': stadium_of_timeframe.name,
                'dia_chi': stadium_of_timeframe.address,
                'sdt': stadium_of_timeframe.owner.phone_number,
                'id': stadium_of_timeframe.pk,
                'khung_gio_dat': timeframe.time_frame.pk
            }
            current_timeframe.append(stadium_detail)


class PasswordChange(View):
    form_class = PasswordChangeForm

    def get(self, request):
        form = self.form_class(request.user)
        context = {
            'form': form
        }
        return render(request, 'password_reset/password_change.html', context)

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Thay đổi mật khẩu thành công!')
        return redirect('password_change')


class AcceptOrderView(View):
    def post(self, request, pk):
        form_type = request.POST.get('form_type')
        order = Order.objects.get(pk=pk)
        type_stadium = order.type_stadium
        order_date = order.order_date
        stadium_timeframe = order.stadium_time_frame
        stadium = order.stadium_time_frame.stadium
        list_field_number = list(range(1, stadium.field_count + 1))
        receiver = order.user
        if receiver:
            sender = request.user

        if form_type == 'accept-input':
            orders_filter = Order.objects.filter(
                stadium_time_frame=stadium_timeframe, order_date=order_date, is_accepted=True)

            for order_filter in orders_filter:
                if order_filter.type_stadium == "7players":
                    order_field_number = order_filter.field_numbers
                    if order_field_number in list_field_number:
                        list_field_number.remove(order_field_number)
                else:
                    for number_of_field in order_filter.field_numbers:
                        if number_of_field in list_field_number:
                            list_field_number.remove(number_of_field)

            if type_stadium == '7players':
                order.field_numbers = list_field_number[0]
                list_field_number.remove(list_field_number[0])
            else:
                if len(list_field_number) >= 3:
                    three_field_merge = list()
                    for number in list_field_number:
                        if len(three_field_merge) < 3:
                            three_field_merge.append(number)
                            # list_field_number.remove(number)
                    order.field_numbers = three_field_merge

            order.is_accepted = True
            order.save()
            notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender}',
                        description=f'Sân {order.stadium_time_frame.stadium.name} bạn đặt vào ngày {order.order_date}, khung giờ {order.stadium_time_frame.time_frame} đã được duyệt! ')

            # Gui thong bao "het san" cho nhung nguoi khac
            if not list_field_number:
                users_list = list()
                orders_not_accepted = Order.objects.filter(
                    stadium_time_frame=stadium_timeframe, order_date=order_date, is_accepted=False)
                for order in orders_not_accepted:
                    user_order = order.user
                    if user_order:
                        users_list.append(user_order)
                receiver = users_list
                notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender}',
                            description=f'Sân {order.stadium_time_frame.stadium.name} bạn đặt vào ngày {order.order_date}, khung giờ {order.stadium_time_frame.time_frame} đã hết sân! Vui lòng chọn khung giờ khác! ')
            messages.success(request, 'Đã duyệt!')

        elif form_type == 'accept-delete':
            order.delete()
            messages.success(request, 'Xóa thành công!')
        return redirect('owner', stadium.pk)


class ChangeNumberOfField(View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        stadium_type = request.POST.get('stadium_type')
        if stadium_type == '7players':
            form = ChangeNumberOfStadium7Form(request.POST)
        else:
            form = ChangeNumberOfStadium11Form(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật vị trí thành công!')
        else:
            messages.error(
                request, 'Vị trí này đã được duyệt! Vui lòng chọn vị trí khác!')

        return redirect('owner', pk=order.stadium_time_frame.stadium.pk)


class Notifications(View):
    def get(self, request):
        user = request.user
        notifications = user.notifications.all()
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        for notification in notifications:
            if notification.unread:
                notification.unread = False
                notification.save()
        context = {
            'fields': fields_by_owner,
            'notifications': notifications
        }
        return render(request, 'book_stadium/notifications.html', context)


class NotificationDetail(View):
    def get(self, request, pk):
        notify = Notification.objects.get(pk=pk)
        fields_by_owner = Stadium.objects.filter(owner=request.user)
        if notify.unread:
            notify.unread = False
            notify.save()
        context = {
            'fields': fields_by_owner,
            'notify': notify
        }

        return render(request, 'book_stadium/notificationDetail.html', context)


class OwnerProfit(View):
    def get(self, request):
        user = request.user
        fields_by_owner = Stadium.objects.filter(owner=user)
        stadium_sales_of_two_recent_months = self.get_stadium_sales_of_two_recent_months(
            fields_by_owner)
        all_stadiums_sales_information_in_lastest_12_months = self.general_stadium_sales_in_lastest_12_months(
            fields_by_owner)
        all_stadium_sales_of_this_month_by_timeframes = self.get_all_stadiums_sales_of_this_month_by_timeframes(
            fields_by_owner)

        if request.is_ajax():
            data = request.GET.get('datasend')
            json_respone = {
                'sales_in_lastest_12_months': all_stadiums_sales_information_in_lastest_12_months,
                'all_stadium_sales_of_this_month_by_timeframes': all_stadium_sales_of_this_month_by_timeframes
            }
            return JsonResponse(json_respone)

        context = {
            'fields': fields_by_owner,
            'stadium_sales_of_two_recent_months': stadium_sales_of_two_recent_months,
        }
        print(stadium_sales_of_two_recent_months)
        return render(request, 'book_stadium/ownerProfit.html', context)

    def get_stadium_sales_of_two_recent_months(self, fields_by_owner):
        current_date = date.today()
        current_month = current_date.month
        last_month = current_date.month - 1
        sales_of_current_month = 0
        sales_of_last_month = 0
        sales = {}

        for stadium in fields_by_owner:
            orders = Order.objects.filter(
                stadium_time_frame__stadium=stadium, is_accepted=True)
            is_same_current_month = False
            is_same_last_month = False

            for order in orders:
                order_month, order_year = self.get_order_month_and_year(order)
                order_price = self.get_order_price(order)
                is_same_current_month = order_month == current_month
                is_same_last_month = order_month == last_month

                if is_same_current_month:
                    sales_of_current_month += order_price
                if is_same_last_month:
                    sales_of_last_month += order_price

        sales['current_month_sales'] = sales_of_current_month
        sales['last_month_sales'] = sales_of_last_month
        print(sales)
        return sales

    def get_stadium_sales_in_lastest_12_months(self, stadium):
        stadium_sales = dict()
        remaining_months = 12
        current_month, current_year = self.get_current_month_and_year()
        oldest_month_in_profit = 0
        oldest_year_in_profit = 0
        is_same_month = False
        is_same_year = False
        orders = Order.objects.filter(
            stadium_time_frame__stadium=stadium).order_by('-order_date')

        if orders:
            for order in orders:
                if remaining_months > 0:
                    order_month, order_year = self.get_order_month_and_year(
                        order)
                    is_same_month = order_month == current_month
                    is_same_year = order_year == current_year
                    order_price = self.get_order_price(order)
                    if not is_same_month or not is_same_year or not stadium_sales:
                        remaining_months -= 1
                        current_month = order_month
                        current_year = order_year
                        stadium_sales = self.set_stadium_name_in_stadium_sales(
                            stadium_sales, stadium)
                        if 'months_and_year' not in stadium_sales:
                            months_and_year = list()
                            stadium_sales['months_and_year'] = months_and_year
                        else:
                            months_and_year = stadium_sales['months_and_year']

                        if 'sales' not in stadium_sales:
                            sales = list()
                            stadium_sales['sales'] = sales
                        else:
                            sales = stadium_sales['sales']

                        months_and_year.append(f'{order_month}-{order_year}')
                        sales.append(order_price)
                    elif is_same_month and is_same_year:
                        stadium_sales['sales'][-1] += order_price

            if remaining_months:
                while remaining_months > 0:
                    current_month -= 1
                    if current_month == 0:
                        current_month = 12
                        current_year -= 1

                    stadium_sales['months_and_year'].append(
                        f'{current_month}-{current_year}')
                    stadium_sales['sales'].append(0)
                    remaining_months -= 1

        else:
            stadium_sales = self.get_stadium_with_no_sales_in_lastest_12_months(
                stadium_sales, stadium, current_year)
        return stadium_sales

    def get_stadium_with_no_sales_in_lastest_12_months(self, stadium_sales, stadium, current_year):
        stadium_sales = self.set_stadium_name_in_stadium_sales(
            stadium_sales, stadium)
        months_and_year = list()
        sales = list()

        for month in range(1, 13):
            months_and_year.append(f'{month}-{current_year}')
            sales.append(0)
        stadium_sales['months_and_year'] = months_and_year
        stadium_sales['sales'] = sales

        return stadium_sales

    def general_stadium_sales_in_lastest_12_months(self, fields_by_owner):
        stadiums_sales_information = list()
        all_stadiums_total_sales = self.get_all_stadiums_total_sales_in_lastest_12_months()

        for stadium in fields_by_owner:
            stadium_sales = self.get_stadium_sales_in_lastest_12_months(
                stadium)
            stadium_name, total_stadium_sales = self.general_stadium_total_sales_in_lastest_12_months(
                stadium_sales)

            all_stadiums_total_sales['stadiums_name'].append(stadium_name)
            all_stadiums_total_sales['sales'].append(total_stadium_sales)

            stadiums_sales_information.append(stadium_sales)
        stadiums_sales_information.append(all_stadiums_total_sales)
        print(json.dumps(stadiums_sales_information, indent=4))
        return stadiums_sales_information

    def set_stadium_name_in_stadium_sales(self, stadium_sales, stadium):
        stadium_sales['stadium_name'] = stadium.name
        return stadium_sales

    def get_order_month_and_year(self, order):
        order_date = order.order_date
        order_month = order_date.month
        order_year = order_date.year
        return [order_month, order_year]

    def general_stadium_total_sales_in_lastest_12_months(self, stadium_sales):
        stadium_name = stadium_sales['stadium_name']
        stadium_sales = stadium_sales['sales']
        total_stadium_sales = 0
        for sales in stadium_sales:
            total_stadium_sales += sales
        return [stadium_name, total_stadium_sales]

    def get_all_stadiums_total_sales_in_lastest_12_months(self):
        all_stadiums_total_sales = dict()
        all_stadiums_name = list()
        all_stadiums_sales = list()

        all_stadiums_total_sales['stadiums_name'] = all_stadiums_name
        all_stadiums_total_sales['sales'] = all_stadiums_sales

        return all_stadiums_total_sales

    def get_current_month_and_year(self):
        current_date = date.today()
        current_month = current_date.month
        current_year = current_date.year

        return [current_month, current_year]

    def get_order_price(self, order):
        order_price = order.stadium_time_frame.price
        return order_price

    def general_stadium_sales_of_this_month_by_timeframes(self, stadium):
        stadium_sales = dict()
        stadium_sales = self.set_stadium_name_in_stadium_sales(
            stadium_sales, stadium)
        current_month, current_year = self.get_current_month_and_year()
        is_same_month = False

        orders = Order.objects.filter(
            stadium_time_frame__stadium=stadium).order_by('order_date')
        stadium_timeframe = StadiumTimeFrame.objects.filter(stadium=stadium)
        all_timeframes = TimeFrame.objects.all()

        # initialization stadium_sales
        if 'timeframes' not in stadium_sales:
            timeframes = list()
            sales_and_number_of_orders = {
                'sales': list(),
                'number_of_orders': list()
            }

            for timeframe in all_timeframes:
                sales = sales_and_number_of_orders['sales']
                number_of_orders = sales_and_number_of_orders['number_of_orders']
                timeframe = str(timeframe)

                timeframes.append(timeframe)
                sales.append(0)
                number_of_orders.append(0)

            stadium_sales['timeframes'] = timeframes
            stadium_sales['sales_and_number_of_orders'] = sales_and_number_of_orders

        if orders:

            for order in orders:
                order_month, order_year = self.get_order_month_and_year(order)
                is_same_month = order_month == current_month
                order_price = self.get_order_price(order)

                if is_same_month:

                    timeframes = stadium_sales['timeframes']
                    sales = stadium_sales['sales_and_number_of_orders']['sales']
                    number_of_orders = stadium_sales['sales_and_number_of_orders']['number_of_orders']

                    order_timeframe = str(order.stadium_time_frame.time_frame)

                    if order_timeframe in timeframes:
                        index_of_timeframe = timeframes.index(order_timeframe)
                        sales[index_of_timeframe] += order_price
                        number_of_orders[index_of_timeframe] += 1

        # print(json.dumps(stadium_sales, indent=4))
        return stadium_sales

    def get_all_stadiums_sales_of_this_month_by_timeframes(self, fields_by_owner):
        all_stadium_sales = list()
        for stadium in fields_by_owner:
            stadium_sales = self.general_stadium_sales_of_this_month_by_timeframes(
                stadium)
            all_stadium_sales.append(stadium_sales)
        print(json.dumps(all_stadium_sales, indent=4))
        return all_stadium_sales
