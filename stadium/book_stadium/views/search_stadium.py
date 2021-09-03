from django.shortcuts import render
from django.core.paginator import Paginator

from book_stadium.models import Stadium
from .book_stadium import BookStadium

from datetime import datetime


class SearchStadium(BookStadium):
    def get(self, request):
        order_form = self.form_class
        user = request.user
        stadiums = Stadium.get_all_stadium()
        stadium_search_result = []
        paginator = Paginator(stadiums, 20)
        today = datetime.today().strftime('%Y/%m/%d')

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        day_search = request.GET.get('day-search')
        time_frame_search = request.GET.get('time_frame')
        address_search = request.GET.get('address-search')
        stadium_name_search = request.GET.get('stadium-name-search')

        stadium_search_result = self.search_stadium(
            day_search, time_frame_search, address_search, stadium_name_search)

        context = {
            'today': today,
            'page_obj': page_obj,
            'order_form': order_form,
            'stadium_search_result': stadium_search_result,
        }

        if user.is_authenticated:
            stadiums_by_owner = Stadium.get_stadium_by_owner(user)
            context['fields'] = stadiums_by_owner
        return render(request, 'book_stadium/search_stadium.html', context)

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
