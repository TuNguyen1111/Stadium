from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from book_stadium.forms import StadiumForm, StadiumTimeFrameForm, StadiumFormForUser, StarRatingForm
from book_stadium.models import Stadium, StadiumTimeFrame, StarRating, StarRatingPermission
from ..messages import *


class StadiumDetail(LoginRequiredMixin, View):
    login_url = 'book_stadium'
    formset = inlineformset_factory(
        Stadium, StadiumTimeFrame, form=StadiumTimeFrameForm, extra=0)

    def get(self, request, pk):
        current_stadium = get_object_or_404(Stadium, pk=pk)

        stadiums_by_owner = Stadium.get_stadium_by_owner(request.user)
        times_and_prices = StadiumTimeFrame.get_stadium_timeframe_by_conditions({"stadium": current_stadium})
        star_rating_of_stadiums = StarRating.get_star_rating_by_stadium(current_stadium, order_by='-star_point')

        form_detail = StadiumForm(instance=current_stadium)
        form_time_frame = self.formset(instance=current_stadium)
        form_detail_for_user = StadiumFormForUser(instance=current_stadium)
        comment_form = StarRatingForm()

        user_vote_permission = get_object_or_404(
            StarRatingPermission, user=request.user, stadium=current_stadium)

        page_info = {
            'fields': stadiums_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
            'form_detail': form_detail,
            'form_time_frame': form_time_frame,
            'form_detail_for_user': form_detail_for_user,
            'comments_of_stadium': star_rating_of_stadiums,
            'comment_form': comment_form,
            'user_vote_permission': user_vote_permission
        }

        return render(
            request,
            'book_stadium/stadium_detail.html',
            page_info,
        )

    def post(self, request, pk):
        form_name = request.POST.get('form_type')
        stadium = get_object_or_404(Stadium, pk=pk)
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

        messages.success(request, UPDATE_INFOR_SUCCESS)
        return redirect('stadium_detail', pk=stadium.pk)
