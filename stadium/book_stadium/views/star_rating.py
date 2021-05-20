from django.http import JsonResponse
from django.views import View
from book_stadium.models import Stadium, StarRating


class StadiumRating(View):
    def get(self, request):
        if request.is_ajax():
            stadium_id = request.GET.get('stadiumId')
            stadium = Stadium.objects.get(pk=stadium_id)
            all_star_rate_of_stadiums = StarRating.objects.filter(
                stadium=stadium).order_by('-star_point')
            total_of_star_type_rated, total_users_rate_of_stadium = self.get_total_of_star_type_rated(
                all_star_rate_of_stadiums)
            amount_of_star_rating_type = self.get_amount_of_star_rating_type_of_stadium(
                all_star_rate_of_stadiums)

            data_response = {
                'total_of_star_type_rated': total_of_star_type_rated,
                'total_users_rate_of_stadium': total_users_rate_of_stadium,
                'amount_of_star_rating_type': amount_of_star_rating_type
            }
            return JsonResponse(data_response)

    def post(self, request):
        if request.is_ajax():
            star_point = int(request.POST.get('starPoint'))
            comment = request.POST.get('commentData')
            stadium_id = int(request.POST.get('stadiumId'))
            stadium = Stadium.objects.get(pk=stadium_id)

            new_user_rate = StarRating.objects.create(
                user=request.user, stadium=stadium, comment=comment, star_point=star_point)
            new_user_rate.save()

            all_star_rate_of_stadiums = StarRating.objects.filter(
                stadium=stadium).order_by('-star_point')
            total_of_star_type_rated, total_users_rate_of_stadium = self.get_total_of_star_type_rated(
                all_star_rate_of_stadiums)

            data_respone = {
                'user_rated_information': {
                    'username': request.user.username,
                    'comment': new_user_rate.comment,
                    'star_point': new_user_rate.star_point,
                },
                'total_of_star_type_rated': total_of_star_type_rated
            }
            return JsonResponse(data_respone)

    def get_total_of_star_type_rated(self, all_star_rate_of_stadiums):
        total_of_star_type_rated = dict()
        total_users_rate_of_stadium = all_star_rate_of_stadiums.count()
        list_of_star_type = self.get_list_of_star_type()

        for star_rate in all_star_rate_of_stadiums:
            star_point = star_rate.star_point
            star_type = list_of_star_type[star_point - 1]

            if star_type in total_of_star_type_rated:
                total_of_star_type_rated[star_type] += 1
            else:
                total_of_star_type_rated[star_type] = 1

        return [total_of_star_type_rated, total_users_rate_of_stadium]

    def get_amount_of_star_rating_type_of_stadium(self, all_star_rate_of_stadiums):
        amount_of_star_rating_type = dict()
        all_users_rated = list()
        amount_of_star_rating_type['all_users_rated'] = all_users_rated
        list_of_star_type = self.get_list_of_star_type()

        for star_rate in all_star_rate_of_stadiums:
            star_point = star_rate.star_point
            star_type = list_of_star_type[star_point - 1]

            if star_type in amount_of_star_rating_type:
                all_users_rate_of_star_type = amount_of_star_rating_type[star_type]
            else:
                all_users_rate_of_star_type = list()
                amount_of_star_rating_type[star_type] = all_users_rate_of_star_type

            user_rated_information = dict()
            user_rated_information['username'] = star_rate.user.username
            user_rated_information['comment'] = star_rate.comment
            user_rated_information['star_point'] = star_rate.star_point

            all_users_rate_of_star_type.append(user_rated_information)
            all_users_rated.append(user_rated_information)
        return amount_of_star_rating_type

    def get_list_of_star_type(self):
        list_of_star_type = ['one_star', 'two_star',
                             'three_star', 'four_star', 'five_star']
        return list_of_star_type
