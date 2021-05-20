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
        # current_stadium = Stadium.objects.get(pk=pk)
        current_stadium = get_object_or_404(Stadium, pk=pk)
        times_and_prices = StadiumTimeFrame.objects.filter(
            stadium=current_stadium)
        formDetail = StadiumForm(instance=current_stadium)
        formTimeFrame = self.formset(instance=current_stadium)
        form_detail_for_user = StadiumFormForUser(instance=current_stadium)
        star_rating_of_stadiums = StarRating.objects.filter(
            stadium=current_stadium).order_by('-star_point')
        comment_form = StarRatingForm()

        page_info = {
            'fields': stadiums_by_owner,
            'stadium': current_stadium,
            'times_and_prices': times_and_prices,
            'formDetail': formDetail,
            'formTimeFrame': formTimeFrame,
            'form_detail_for_user': form_detail_for_user,
            'comments_of_stadium': star_rating_of_stadiums,
            'comment_form': comment_form
        }
        return render(
            request,
            'book_stadium/stadiumDetail.html',
            page_info,
        )

    def post(self, request, pk):
        formname = request.POST.get('form_type')
        stadium = Stadium.objects.get(pk=pk)
        owner = request.user

        if formname == 'form_detail':
            form_detail = StadiumForm(
                request.POST, request.FILES, instance=stadium)

            if form_detail.is_valid():
                # như trên, đẩy owner vào.
                instance = form_detail.save(commit=False)
                instance.owner = owner
                instance.save()
            else:
                print(form_detail.errors)

        elif formname == 'form_time':
            formTimeFrame = self.formset(request.POST, instance=stadium)

            if formTimeFrame.is_valid():
                formTimeFrame.save()

        elif formname == 'delete-input':
            stadium.delete()
            return redirect('book_stadium')

        messages.success(request, 'Cập nhật thành công!')
        return redirect('stadium_detail', pk=stadium.pk)
