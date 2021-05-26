import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone

from book_stadium.forms import ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form
from book_stadium.models import Order, Stadium, TimeFrame, Roles, TypeOfStadium


class OwnerPage(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "home"
    template_name = 'book_stadium/owner.html'

    def get(self, request, pk):
        update_stadium_7players_form = ChangeNumberOfStadium7Form()
        update_stadium_11players_form = ChangeNumberOfStadium11Form()

        stadiums_by_owner = Stadium.objects.filter(owner=request.user)
        stadium = get_object_or_404(Stadium, pk=pk)

        orders_of_stadium = self.general_orders(stadium)
        # tao dict voi moi ngay co order

        context = {
            'fields': stadiums_by_owner,
            'orders_of_stadium': orders_of_stadium,
            'update_stadium_7players_form': update_stadium_7players_form,
            'update_stadium_11players_form': update_stadium_11players_form
        }
        return render(request,
                      'book_stadium/owner.html',
                      context,
                      )

    def general_orders(self, stadium):
        orders_of_stadium = list()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        is_today_in_orders_of_stadium = False
        date_format = '%Y/%m/%d'

        all_time_frames = TimeFrame.objects.all()
        orders = Order.objects.filter(stadium_time_frame__stadium=stadium, order_date__gte=today)\
                              .order_by('order_date')

        for order in orders:
            order_date = order.order_date
            if today == order_date:
                is_today_in_orders_of_stadium = True
                break

        if not is_today_in_orders_of_stadium:
            first_order = {
                'ngay': 'Hôm nay',
                'khung_gio': {}
            }
            orders_of_stadium.append(first_order)
            time_frames = orders_of_stadium[0]['khung_gio']

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

        for order in orders:
            order_date = order.order_date
            is_same_day = False

            if orders_of_stadium:
                # lay ra order cuoi va check xem co cung ngay hay khong
                last_order = orders_of_stadium[-1]
                if last_order['ngay'] == 'Hôm nay':
                    last_order['ngay'] = today.strftime(date_format)
                elif last_order['ngay'] == 'Ngày mai':
                    last_order['ngay'] = tomorrow.strftime(date_format)
                is_same_day = last_order['ngay'] == order_date.strftime(
                    date_format)

            if is_same_day:
                current_order = orders_of_stadium[-1]
            else:
                current_order = {
                    'ngay': order_date.strftime(date_format),
                    'khung_gio': {}
                }

                if order_date == today:
                    current_order['ngay'] = 'Hôm nay'
                elif order_date == tomorrow:
                    current_order['ngay'] = 'Ngày mai'
                orders_of_stadium.append(current_order)

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
                        'ao_tap': order.pitch_clothes,
                        'loai_san': order.type_stadium,
                        'tong_san': stadium.field_count
                    }

                    if order.type_stadium == TypeOfStadium.SMALL:
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
        orders_of_stadium = self.get_remaining_fields(
            orders_of_stadium, stadium)

        return orders_of_stadium

    def get_remaining_fields(self, orders_of_stadium, stadium):
        for order in orders_of_stadium:
            for key, time_frame in order['khung_gio'].items():
                count_accept_user = 0
                for user in time_frame['nguoi_dat']:
                    if user['da_duyet']:
                        if user['loai_san'] == TypeOfStadium.SMALL:
                            count_accept_user += 1
                        else:
                            count_accept_user += 3
                remaining_fields = stadium.field_count - count_accept_user
                time_frame['con_trong'] = remaining_fields
        return orders_of_stadium

    def test_func(self):
        return self.request.user.role == Roles.OWNER
