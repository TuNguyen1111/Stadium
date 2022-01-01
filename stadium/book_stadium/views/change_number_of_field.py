from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from book_stadium.forms import ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form
from book_stadium.models import Order, TypeOfStadium
from ..messages import *


class ChangeNumberOfField(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        stadium_type = request.POST.get('stadium_type')

        if stadium_type == TypeOfStadium.SMALL:
            form = ChangeNumberOfStadium7Form(request.POST)
        else:
            form = ChangeNumberOfStadium11Form(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, UPDATE_FIELD_SUCCESS)
        else:
            messages.error(
                request, CHOOSE_ANOTHER_FIELD)

        return redirect('owner', pk=order.stadium_time_frame.stadium.pk)
