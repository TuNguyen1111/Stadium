from django.shortcuts import render
from book_stadium.forms import UserCreationForm
from django.views import View


class Home(View):
    form_class = UserCreationForm
    template_name = 'book_stadium/home.html'
    # stadiums_by_owner = Stadium.objects.filter(owner=request.user)

    def get(self, request):
        context = {
            'register_form': self.form_class,
        }
        return render(
            request,
            self.template_name,
            context
        )
