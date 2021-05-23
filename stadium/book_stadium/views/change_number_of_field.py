from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from book_stadium.forms import ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form
from book_stadium.models import Order, TypeOfStadium


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
            messages.success(request, 'Cập nhật vị trí thành công!')
        else:
            messages.error(
                request, 'Vị trí này đã được duyệt! Vui lòng chọn vị trí khác!')

        return redirect('owner', pk=order.stadium_time_frame.stadium.pk)
