import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View

from book_stadium.models import Order, Stadium, TimeFrame, User, Roles, TypeOfStadium


class OwnerProfit(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'home'

    def get(self, request, pk):
        # REVIEW: Ở đây nên tách thành 2 view riêng biệt chứ không nên phân biệt bằng request.is_ajax()
        # Lý do: 2 view này cần các thông tin khác nhau:
        #   - View ajax cần 'sales_information_in_lastest_12_months', 'sales_of_this_month_by_timeframes'
        #   - View thường cần 'stadium_sales_of_two_recent_months'
        #   => Tách ra sẽ hiệu quả hơn, mỗi view chỉ cần gọi hàm tương ứng để lấy đủ data cần thiết
        # Hoặc có viết cùng view thì cũng nên tách ra kiểu:
        # if request.is_ajax():
        #   return self.get_ajax_response()
        # else:
        #   return self.get_normal_response()

        user = get_object_or_404(User, pk=pk)
        stadiums_by_owner = Stadium.objects.filter(owner=user)

        stadium_sales_of_two_recent_months = self.get_stadium_sales_of_two_recent_months(
            stadiums_by_owner)
        sales_information_in_lastest_12_months = self.general_stadium_sales_information_in_lastest_12_months(
            stadiums_by_owner)
        sales_of_this_month_by_timeframes = self.get_stadiums_sales_of_this_month_by_timeframes(
            stadiums_by_owner)
        print(json.dumps(sales_information_in_lastest_12_months, indent=4))
        if request.is_ajax():
            json_respone = {
                'sales_information_in_lastest_12_months': sales_information_in_lastest_12_months,
                'sales_of_this_month_by_timeframes': sales_of_this_month_by_timeframes
            }
            return JsonResponse(json_respone)

        context = {
            'fields': stadiums_by_owner,
            'stadium_sales_of_two_recent_months': stadium_sales_of_two_recent_months,
        }
        return render(request, 'book_stadium/owner_profit.html', context)

    def get_stadium_sales_of_two_recent_months(self, stadiums_by_owner):
        current_date = date.today()
        current_month = current_date.month
        last_month = current_date.month - 1
        sales_of_current_month = 0
        sales_of_last_month = 0
        sales = {}

        for stadium in stadiums_by_owner:
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
        return sales

    def get_stadium_sales_information_in_lastest_12_months(self, stadium):
        stadium_sales = dict()
        remaining_months = 12
        current_month, current_year = self.get_current_month_and_year()
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
            stadium_sales = self.get_stadium_with_no_sales_information_in_lastest_12_months(
                stadium_sales, stadium, current_year)
        return stadium_sales

    def get_stadium_with_no_sales_information_in_lastest_12_months(self, stadium_sales, stadium, current_year):
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

    def general_stadium_sales_information_in_lastest_12_months(self, stadiums_by_owner):
        stadiums_sales_information = list()
        stadiums_sales = self.get_stadiums_sales_information_in_lastest_12_months()

        for stadium in stadiums_by_owner:
            stadium_sales = self.get_stadium_sales_information_in_lastest_12_months(
                stadium)
            stadium_name, total_stadium_sales = self.summary_stadium_sales_information_in_lastest_12_months(
                stadium_sales)

            stadiums_sales['stadiums_name'].append(stadium_name)
            stadiums_sales['sales'].append(total_stadium_sales)
            stadiums_sales_information.append(stadium_sales)

        stadiums_sales_information.append(stadiums_sales)
        return stadiums_sales_information

    def set_stadium_name_in_stadium_sales(self, stadium_sales, stadium):
        stadium_sales['stadium_name'] = stadium.name
        return stadium_sales

    def get_order_month_and_year(self, order):
        order_date = order.order_date
        order_month = order_date.month
        order_year = order_date.year
        return [order_month, order_year]

    def summary_stadium_sales_information_in_lastest_12_months(self, stadium_sales):
        stadium_name = stadium_sales['stadium_name']
        stadium_sales = stadium_sales['sales']
        total_stadium_sales = 0

        for sales in stadium_sales:
            total_stadium_sales += sales
        return [stadium_name, total_stadium_sales]

    def get_stadiums_sales_information_in_lastest_12_months(self):
        stadiums_sales = dict()
        stadiums_name = list()
        sales = list()

        stadiums_sales['stadiums_name'] = stadiums_name
        stadiums_sales['sales'] = sales

        return stadiums_sales

    def get_current_month_and_year(self):
        current_date = date.today()
        current_month = current_date.month
        current_year = current_date.year

        return [current_month, current_year]

    def get_order_price(self, order):
        if order.type_stadium == TypeOfStadium.BIG:
            order_price = order.stadium_time_frame.price * 3
        else:
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
        stadium_timeframes = TimeFrame.objects.all()

        # initialization stadium_sales
        if 'timeframes' not in stadium_sales:
            timeframes = list()
            sales_and_number_of_orders = {
                'sales': list(),
                'number_of_orders': list()
            }

            for timeframe in stadium_timeframes:
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
        return stadium_sales

    def get_stadiums_sales_of_this_month_by_timeframes(self, stadiums_by_owner):
        stadiums_sales = list()

        for stadium in stadiums_by_owner:
            stadium_sales = self.general_stadium_sales_of_this_month_by_timeframes(
                stadium)
            stadiums_sales.append(stadium_sales)

        return stadiums_sales

    def test_func(self):
        return self.request.user.role == Roles.OWNER
