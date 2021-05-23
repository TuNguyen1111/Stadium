from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import UserCreationForm

# Register your models here.


class UserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm
    list_display = ['id', 'phone_number', 'email', 'username', 'role']

    # None is a Header of User Detail in Admin page
    fieldsets = (
        (None, {'fields': ('username', 'password', 'phone_number',
                           'role', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser', 'phone_number', 'username', 'role')}
         ),
    )
    list_filter = ["is_superuser", "role"]


class AdminTimeFrame(admin.ModelAdmin):
    list_display = ['stadium', 'time_frame', 'price']


admin.site.register(User, UserAdmin)
admin.site.register(Stadium)
admin.site.register(TimeFrame)
admin.site.register(StadiumTimeFrame, AdminTimeFrame)
admin.site.register(Order)
admin.site.register(StarRating)
admin.site.register(StarRatingPermission)
