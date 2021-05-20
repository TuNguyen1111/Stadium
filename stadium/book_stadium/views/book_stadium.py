from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.core.paginator import Paginator
from datetime import datetime
from notifications.signals import notify
from swapper import load_model
import datetime
from book_stadium.forms import OrderForm, UserCreationForm
from book_stadium.models import Order, Stadium, StadiumTimeFrame

Notification = load_model('notifications', 'Notification')


class BookStadium(ListView):
    form_class = OrderForm

    def get(self, request):
        register_form = UserCreationForm
        order_form = self.form_class
        stadium_timeframes = StadiumTimeFrame.objects.filter(
            is_open=True).order_by('time_frame__start_time')
        all_stadiums = []
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
            stadiums_by_owner = Stadium.objects.filter(owner=request.user)
        else:
            stadiums_by_owner = ''
        # print(json.dumps(all_stadiums, indent=4))

        context = {
            'fields': stadiums_by_owner,
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
                notify.send(sender, recipient=receiver, verb=f'Thông báo từ {sender_name}',
                            description=f'{sender_name} đã đặt sân {stadium_name_notification} của bạn vào ngày {date_notification}, khung giờ {timeframe_notification}')
            else:
                pass
                # sender = User.objects.get(pk=10)

            messages.success(request, 'Đặt sân thành công!')

        else:
            messages.warning(request, 'Vui long chon khung gio khac!')

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

                    current_timeframe = self.check_is_same_stadium(
                        current_timeframe, stadium_of_timeframe, timeframe)
        return all_stadiums

    def check_is_same_stadium(self, current_timeframe, stadium_of_timeframe, timeframe):
        if len(current_timeframe) < 3:
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
        return current_timeframe

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
        time = str(timeframe.time_frame)

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
        stadium_obj['anh'] = stadium_of_timeframe.image.url
        stadium_obj['ten'] = stadium_of_timeframe.name
        stadium_obj['dia_chi'] = stadium_of_timeframe.address
        stadium_obj['sdt'] = stadium_of_timeframe.owner.phone_number
        stadium_obj['id'] = stadium_of_timeframe.pk
        search_obj['khung_gio'][time].append(stadium_obj)

        return stadium_search_result
