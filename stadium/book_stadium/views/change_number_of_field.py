from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from book_stadium.forms import ChangeNumberOfStadium7Form, ChangeNumberOfStadium11Form
from book_stadium.models import Order


class ChangeNumberOfField(View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        stadium_type = request.POST.get('stadium_type')

        if stadium_type == '7players':
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
