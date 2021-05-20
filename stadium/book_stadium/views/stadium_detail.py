from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from book_stadium.forms import StadiumForm, StadiumTimeFrameForm, StadiumFormForUser, StarRatingForm
from book_stadium.models import Stadium, StadiumTimeFrame, StarRating


class StadiumDetail(LoginRequiredMixin, View):
    login_url = 'home'
    formset = inlineformset_factory(
        Stadium, StadiumTimeFrame, form=StadiumTimeFrameForm, extra=0)

    def get(self, request, pk):
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)
        current_stadium = get_object_or_404(Stadium, pk=pk)
        times_and_prices = StadiumTimeFrame.objects.filter(
            stadium=current_stadium)
        form_detail = StadiumForm(instance=current_stadium)
        form_time_frame = self.formset(instance=current_stadium)
        form_detail_for_user = StadiumFormForUser(instance=current_stadium)
        star_rating_of_stadiums = StarRating.objects.filter(
            stadium=current_stadium).order_by('-star_point')
        comment_form = StarRatingForm()

        page_info = {
            'fields': stadiums_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
            'form_detail': form_detail,
            'form_time_frame': form_time_frame,
            'form_detail_for_user': form_detail_for_user,
            'comments_of_stadium': star_rating_of_stadiums,
            'comment_form': comment_form
        }
        return render(
            request,
            'book_stadium/stadium_detail.html',
            page_info,
        )

    def post(self, request, pk):
        form_name = request.POST.get('form_type')
        stadium = Stadium.objects.get(pk=pk)
        owner = request.user

        if form_name == 'form_detail':
            form_detail = StadiumForm(
                request.POST, request.FILES, instance=stadium)

            if form_detail.is_valid():
                instance = form_detail.save(commit=False)
                instance.owner = owner
                instance.save()
            else:
                context = {
                    'form_detail': form_detail
                }
                return render(request, 'book_stadium/stadium_detail.html', context)

        elif form_name == 'form_time':
            form_time_frame = self.formset(request.POST, instance=stadium)

            if form_time_frame.is_valid():
                form_time_frame.save()

        elif form_name == 'delete_input':
            stadium.delete()
            return redirect('book_stadium')

        messages.success(request, 'Cập nhật thành công!')
        return redirect('stadium_detail', pk=stadium.pk)
