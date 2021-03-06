import datetime
from notifications.signals import notify
from swapper import load_model

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.core.paginator import Paginator

from book_stadium.forms import OrderForm
from book_stadium.models import Order, Stadium, StadiumTimeFrame
from ..messages import *
from .base import Base

Notification = load_model('notifications', 'Notification')


class BookStadium(Base, ListView):
    form_class = OrderForm

    def get(self, request):
        order_form = self.form_class

        stadium_timeframes = StadiumTimeFrame.get_stadium_timeframe_by_conditions({"is_open": True}, order_by='time_frame__start_time')
        context = self.get_default_context()

        if stadium_timeframes:
            all_stadiums = self.put_out_null_stadiums_and_timesframe(
                stadium_timeframes)
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
                stadiums_by_owner = Stadium.get_stadium_by_owner(request.user)
            else:
                stadiums_by_owner = ''

            context.update({
                'fields': stadiums_by_owner,
                'stadiums': all_stadiums,
                'page_obj': page_obj,
                'order_form': order_form,
                'stadium_search_result': stadium_search_result,
            })
        else:
            context['have_available_stadium'] = False

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
                notify.send(sender, recipient=receiver, verb=f'Th??ng b??o t??? {sender_name}',
                            description=(f'{sender_name} ???? ?????t s??n {stadium_name_notification} c???a b???n v??o ng??y {date_notification}, '
                                         'khung gi??? {timeframe_notification}'))
            else:
                pass

            messages.success(request, ORDER_SUCCESS)

        else:
            messages.warning(request, CHOOSE_ANOTHER_TIMEFRAME)

        return redirect('book_stadium')

    def put_out_null_stadiums_and_timesframe(self, stadium_timeframes):
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
                stadium_of_timeframe = timeframe.stadium
                total_stadium_fields = stadium_of_timeframe.field_count
                orders = Order.objects.filter(stadium_time_frame=timeframe, order_date=current_day, is_accepted=True)
                is_in_6_to_17 = (
                    timeframe.time_frame.start_time >= datetime.time(6) and
                    timeframe.time_frame.end_time <= datetime.time(17)
                )

                # Count how many order this timeframe have
                if orders:
                    total_order_accepted = len(orders)
                    if total_order_accepted >= total_stadium_fields:
                        continue

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

                current_timeframe = self.check_is_same_stadium(current_timeframe, stadium_of_timeframe, timeframe)
        return all_stadiums

    def check_is_same_stadium(self, current_timeframe, stadium_of_timeframe, timeframe):
        max_stadium = 4
        if len(current_timeframe) < max_stadium:
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
            return current_timeframe[:3]

    def search_stadium(self, day_search, time_frame_search, address_search, stadium_name_search):
        stadium_search_result = []

        if day_search:
            conditions = {}
            day_search = day_search.replace('/', '-')

            if time_frame_search:
                conditions['time_frame'] = time_frame_search
            if address_search:
                conditions['stadium__address'] = address_search
            if stadium_name_search:
                conditions['stadium__name'] = stadium_name_search

            stadiums_timeframe_search = StadiumTimeFrame.get_stadium_timeframe_by_conditions(conditions)

            for stadium_timeframe in stadiums_timeframe_search:
                # count how many order is accepted, if >= stadium field_count then no more field to order
                order_conditions = {
                    'stadium_time_frame': stadium_timeframe,
                    'order_date': day_search,
                    'is_accepted': True
                }
                orders = Order.get_order_by_conditions(order_conditions)
                stadium = stadium_timeframe.stadium
                if orders:
                    if len(orders) >= stadium.field_count:
                        continue

                self.add_stadium_obj(
                    stadium_search_result, day_search, stadium, stadium_timeframe)

        return stadium_search_result

    def add_stadium_obj(self, stadium_search_result, day_search, stadium, stadium_timeframe):
        time = str(stadium_timeframe.time_frame)

        if stadium_search_result:
            search_obj = stadium_search_result[-1]
        else:
            search_obj = {}
            search_obj['ngay'] = day_search
            timeframe_obj = {}
            search_obj['khung_gio'] = timeframe_obj
            all_stadiums_obj = []
            timeframe_obj[time] = all_stadiums_obj
            stadium_search_result.append(search_obj)

        stadium_obj = {}
        stadium_obj['anh'] = stadium.image.url
        stadium_obj['ten'] = stadium.name
        stadium_obj['dia_chi'] = stadium.address
        stadium_obj['sdt'] = stadium.owner.phone_number
        stadium_obj['id'] = stadium.pk
        stadium_obj['khung_gio_dat'] = stadium_timeframe.time_frame.pk
        search_obj['khung_gio'][time].append(stadium_obj)

        return stadium_search_result

    def get_default_context(self):
        context = super().get_default_context()
        context['have_available_stadium'] = True

        return context
