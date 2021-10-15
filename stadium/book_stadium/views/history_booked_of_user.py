from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views import View

from book_stadium.models import Order, User


class HistoryBookedOfUser(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        start_day = request.GET.get('start-day')
        end_day = request.GET.get('end-day')
        user_orders = Order.get_order_by_user(user)

        conditions = {}

        if start_day:
            start_day = start_day.replace('/', '-')
            conditions['order_date__gte'] = start_day

        if end_day:
            end_day = end_day.replace('/', '-')
            conditions['order_date__lte'] = end_day

        user_orders = user_orders.filter(
            **conditions).select_related('stadium_time_frame').order_by('order_date')

        orders_of_user = self.general_order_of_user(user_orders)

        context = {
            'orders_of_user': orders_of_user
        }
        return render(request, 'book_stadium/history_booked_of_user.html', context)

    def post(self, request, pk):
        user = request.user
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect('history_booked', user.pk)

    def general_order_of_user(self,  user_orders):
        orders_of_user = []
        order_date_format = '%Y/%m/%d'
        for order in user_orders:
            is_same_day = False

            if orders_of_user:
                last_order = orders_of_user[-1]
                is_same_day = last_order['ngay'] == order.order_date.strftime(
                    order_date_format)

            if is_same_day:
                current_order = orders_of_user[-1]
            else:
                current_order = {
                    'ngay':  order.order_date.strftime(order_date_format),
                    'khung_gio': {}
                }
                orders_of_user.append(current_order)

            if order.stadium_time_frame:
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
        return orders_of_user
