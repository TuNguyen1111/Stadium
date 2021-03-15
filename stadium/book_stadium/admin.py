from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("username", 'role')
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'is_superuser', 'is_active')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'is_superuser', 'phone_number', 'email', 'role')}
            ),
        )

    list_filter = ["is_superuser", "role"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Stadium)
admin.site.register(TimeFrame)
admin.site.register(StadiumTimeFrame)
admin.site.register(Order)