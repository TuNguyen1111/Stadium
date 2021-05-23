from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from book_stadium.forms import StadiumForm
from book_stadium.models import Stadium, StadiumTimeFrame, TimeFrame, Roles, StarRatingPermission, User


class CreateStadium(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'home'
    create_stadium_form = StadiumForm

    def get(self, request):
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)
        form = self.create_stadium_form

        context = {
            'fields': stadiums_by_owner,
            'form': form
        }
        return render(
            request,
            'book_stadium/create_stadium.html',
            context)

    def post(self, request):
        create_stadium_form = self.create_stadium_form(
            request.POST, request.FILES)
        owner = request.user

        if create_stadium_form.is_valid():
            # nếu form valid thì đẩy owner bằng request.user rồi mới save nha
            new_stadium = create_stadium_form.save(commit=False)
            new_stadium.owner = owner
            new_stadium.save()

        stadium = get_object_or_404(Stadium, pk=new_stadium.pk)
        time_frames = TimeFrame.objects.all()

        for timeframe in time_frames:
            stadium_time_frame = StadiumTimeFrame.objects.create(
                stadium=stadium,
                time_frame=timeframe,
                price=300_000,
            )
            stadium_time_frame.save()
        self.create_permission_vote_for_user(stadium)

        messages.success(request, 'Tạo sân thành công!')
        return redirect('stadium_detail', pk=stadium.pk)

    def create_permission_vote_for_user(self, stadium):
        users = User.objects.all()
        for user in users:
            if user.role == Roles.PLAYER:
                user_permission_vote = StarRatingPermission.objects.create(
                    user=user, stadium=stadium)
            else:
                user_permission_vote = StarRatingPermission.objects.create(
                    user=user, stadium=stadium, can_rate=False)
            user_permission_vote.save()

    def test_func(self):
        return self.request.user.role == Roles.OWNER
