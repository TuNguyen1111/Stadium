from notifications.signals import notify
from swapper import load_model

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from book_stadium.models import Order, TypeOfStadium
from ..messages import *


class AcceptOrderView(View):
    def post(self, request, pk):
        form_type = request.POST.get('form_type')
        order = get_object_or_404(Order, pk=pk)

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
                if order_filter.type_stadium == TypeOfStadium.SMALL:
                    order_field_number = order_filter.field_numbers

                    if order_field_number in list_field_number:
                        list_field_number.remove(order_field_number)
                else:
                    for number_of_field in order_filter.field_numbers:
                        if number_of_field in list_field_number:
                            list_field_number.remove(number_of_field)

            if type_stadium == TypeOfStadium.SMALL:
                order.field_numbers = list_field_number[0]
                list_field_number.remove(list_field_number[0])
            else:
                if len(list_field_number) >= 3:
                    three_field_merge = list()

                    for number in list_field_number:
                        if len(three_field_merge) < 3:
                            three_field_merge.append(number)
                    order.field_numbers = three_field_merge

            order.is_accepted = True
            order.save()

            notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender}',
                        description=(f'Sân {order.stadium_time_frame.stadium.name} bạn đặt vào ngày {order.order_date}, '
                                     f'khung giờ {order.stadium_time_frame.time_frame} '
                                     'đã được duyệt! '))

            # Gui thong bao "het san" cho nhung nguoi khac
            if not list_field_number:
                users_list = list()
                orders_not_accepted = Order.objects.filter(
                    stadium_time_frame=stadium_timeframe, order_date=order_date, is_accepted=False).select_related('user')

                for order in orders_not_accepted:
                    user_order = order.user
                    if user_order:
                        users_list.append(user_order)
                receiver = users_list
                notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender}',
                            description=(f'Sân {order.stadium_time_frame.stadium.name} bạn đặt vào ngày {order.order_date}, '
                                         f'khung giờ {order.stadium_time_frame.time_frame} đã hết sân! '
                                         'Vui lòng chọn khung giờ khác! '))
            messages.success(request, ACCEPTED_ORDER)

        elif form_type == 'accept-delete':
            order.delete()
            messages.success(request, DELETED_ORDER)
        return redirect('owner', stadium.pk)
