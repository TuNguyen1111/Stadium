from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

        # def save(self, commit=True):
        #     # Save the provided password in hashed format
        #     user = super(UserCreationForm, self).save(commit=False)
        #     user.set_password(self.cleaned_data["password"])
        #     if commit:
        #         user.save()
        #     return user


# class RegisterForm(UserCreationForm):
