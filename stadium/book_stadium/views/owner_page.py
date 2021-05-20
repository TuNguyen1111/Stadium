from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone
from datetime import datetime
import datetime
from book_stadium.forms import ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form
from book_stadium.models import Order, Stadium, TimeFrame, Roles


class OwnerPage(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "home"
    template_name = 'book_stadium/owner.html'

    def get(self, request, pk):
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)
        stadium = get_object_or_404(Stadium, pk=pk)
        all_time_frames = TimeFrame.objects.all()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        date_format = '%Y/%m/%d'
        orders = Order.objects.filter(stadium_time_frame__stadium=stadium, order_date__gte=timezone.now())\
                              .order_by('order_date')

        update_stadium_7players_form = ChangeNumberOfStadium7Form()
        update_stadium_11players_form = ChangeNumberOfStadium11Form()

        all_orders = self.general_orders(orders, stadium)
        # tao dict voi moi ngay co order
        for order in orders:
            is_same_day = False

            if all_orders:
                # lay ra order cuoi va check xem co cung ngay hay khong
                last_order = all_orders[-1]
                if last_order['ngay'] == 'Hôm nay':
                    last_order['ngay'] = today.strftime(date_format)
                elif last_order['ngay'] == 'Ngày mai':
                    last_order['ngay'] = tomorrow.strftime(date_format)
                is_same_day = last_order['ngay'] == order.order_date.strftime(
                    date_format)

            if is_same_day:
                current_order = all_orders[-1]
            else:
                current_order = {
                    'ngay': order.order_date.strftime(date_format),
                    'khung_gio': {}
                }

                if order.order_date == today:
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

        context = {
            'fields': stadiums_by_owner,
            'all_orders': all_orders,
            'update_stadium_7players_form': update_stadium_7players_form,
            'update_stadium_11players_form': update_stadium_11players_form
        }
        return render(request,
                      'book_stadium/owner.html',
                      context,
                      )

    def general_orders(self, orders, stadium):
        all_orders = []
        all_time_frames = TimeFrame.objects.all()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        is_today_in_all_orders = False

        for order in orders:
            if today == order.order_date:
                is_today_in_all_orders = True
                break

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
        return all_orders

    def test_func(self):
        return self.request.user.role == Roles.OWNER