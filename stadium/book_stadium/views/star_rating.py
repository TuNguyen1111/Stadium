from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from book_stadium.models import Stadium, StarRating, StarRatingPermission


class StadiumRating(View):
    def get(self, request):
        if request.is_ajax():
            current_user = request.user
            stadium_id = request.GET.get('stadiumId')
            stadium = get_object_or_404(Stadium, pk=stadium_id)
            stars_rate_of_stadium = StarRating.get_star_rating_by_stadium(stadium, order_by='-star_point')

            stars_type_rated_numbers = self.get_stars_type_rated_numbers(
                stars_rate_of_stadium)
            summary_of_stars_type = self.set_current_user_rated_to_the_top(
                current_user, stars_rate_of_stadium)

            data_response = {
                'stars_type_rated_numbers': stars_type_rated_numbers,
                'summary_of_stars_type': summary_of_stars_type
            }
            return JsonResponse(data_response)

    def post(self, request):
        if request.is_ajax():
            current_user = request.user
            star_point = request.POST.get('starPoint')
            comment = request.POST.get('commentData')
            stadium_id = request.POST.get('stadiumId')
            stadium = get_object_or_404(Stadium, pk=stadium_id)
            user = request.user

            new_user_rate = StarRating.create_user_star_rating(user, stadium, comment, star_point)

            user_rate_permission = get_object_or_404(
                StarRatingPermission, user=user, stadium=stadium)
            user_rate_permission.can_rate = False
            user_rate_permission.save()

            stars_rate_of_stadium = StarRating.get_star_rating_by_stadium(stadium, order_by='-star_point')
            stars_type_rated_numbers = self.get_stars_type_rated_numbers(
                stars_rate_of_stadium)
            summary_of_stars_type = self.set_current_user_rated_to_the_top(
                current_user, stars_rate_of_stadium)

            data_respone = {
                'user_rated_information': {
                    'username': user.username,
                    'user_id': user.id,
                    'comment': new_user_rate.comment,
                    'star_point': new_user_rate.star_point,
                    'user_rate_permission': user_rate_permission.can_rate
                },
                'stars_type_rated_numbers': stars_type_rated_numbers,
                'summary_of_stars_type': summary_of_stars_type
            }
            return JsonResponse(data_respone)

    def get_stars_type_rated_numbers(self, stars_rate_of_stadium):
        stars_type_rated_numbers = dict()
        stars_type = self.get_stars_type()

        for star_rate in stars_rate_of_stadium:
            star_point = star_rate.star_point
            star_type = stars_type[star_point - 1]

            if star_type in stars_type_rated_numbers:
                stars_type_rated_numbers[star_type] += 1
            else:
                stars_type_rated_numbers[star_type] = 1

        return stars_type_rated_numbers

    def summary_of_stadium_stars_type(self, stars_rate_of_stadium):
        summary_of_stars_type = dict()
        users_rated = list()
        summary_of_stars_type['users_rated'] = users_rated
        stars_type = self.get_stars_type()

        for star_rate in stars_rate_of_stadium:
            star_point = star_rate.star_point
            star_type = stars_type[star_point - 1]

            if star_type in summary_of_stars_type:
                star_type_users_rated = summary_of_stars_type[star_type]
            else:
                star_type_users_rated = list()
                summary_of_stars_type[star_type] = star_type_users_rated

            user_rated_information = dict()
            user_rated_information['username'] = star_rate.user.username
            user_rated_information['comment'] = star_rate.comment
            user_rated_information['star_point'] = star_rate.star_point
            user_rated_information['user_id'] = star_rate.user.id

            star_type_users_rated.append(user_rated_information)
            users_rated.append(user_rated_information)

        return summary_of_stars_type

    def set_current_user_rated_to_the_top(self, current_user, stars_rate_of_stadium):
        summary_of_stars_type = self.summary_of_stadium_stars_type(
            stars_rate_of_stadium)

        for star_type, users_rated_information in summary_of_stars_type.items():
            for index, user_rated in enumerate(users_rated_information):
                if current_user.id == user_rated['user_id']:
                    users_rated_information[index], users_rated_information[
                        0] = users_rated_information[0], users_rated_information[index]
        return summary_of_stars_type

    def get_stars_type(self):
        stars_type = ['one_star', 'two_star',
                      'three_star', 'four_star', 'five_star']
        return stars_type


class StadiumRatingEdit(StadiumRating):
    def post(self, request):
        if request.is_ajax():
            new_star_point = request.POST.get('starPoint')
            new_comment = request.POST.get('commentData')
            stadium_id = request.POST.get('stadiumId')
            current_user = request.user

            stadium = get_object_or_404(Stadium, pk=stadium_id)
            user_rate_permission = get_object_or_404(
                StarRatingPermission, user=current_user, stadium=stadium)
            user_rated = get_object_or_404(
                StarRating, user=current_user, stadium=stadium)

            user_rated.comment = new_comment
            user_rated.star_point = new_star_point
            user_rated.save()

            stars_rate_of_stadium = StarRating.get_star_rating_by_stadium(stadium, order_by='-star_point')
            summary_of_stars_type = self.set_current_user_rated_to_the_top(
                current_user, stars_rate_of_stadium)
            stars_type_rated_numbers = self.get_stars_type_rated_numbers(
                stars_rate_of_stadium)

            data_respone = {
                'user_rated_information_edited': {
                    'username': current_user.username,
                    'user_id': current_user.id,
                    'comment': user_rated.comment,
                    'star_point': user_rated.star_point,
                    'user_rate_permission': user_rate_permission.can_rate
                },
                'summary_of_stars_type': summary_of_stars_type,
                'stars_type_rated_numbers': stars_type_rated_numbers,
            }

            return JsonResponse(data_respone)
