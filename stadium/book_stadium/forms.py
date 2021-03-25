from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Stadium, StadiumTimeFrame
from crispy_forms.helper import FormHelper

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


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'stadium_time_frame', 'field_number', 'order_datetime', 'customer_phone_number', 'is_accepted']
        labels = {
            'user': 'Người đặt:',
            'stadium_time_frame': 'Khung giờ:',
            'field_number': 'Sân số',
            'order_datetime': 'Ngày đặt',
            'customer_phone_number': 'Số điện thoại'
        }


class StadiumForm(forms.ModelForm):
    class Meta:
        model = Stadium
        fields = ['name', 'address', 'field_count']
        labels = {
            'name': 'Tên sân',
            'address': 'Địa chỉ',
            'field_count': 'Số sân có thể đặt'
        }
        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(
               attrs={
                   'class': 'form-control',
                   'id': '{}'.format(field),
                   'disabled': True,
               }
           )

class StadiumTimeFrameForm(forms.ModelForm):
    class Meta:
        model = StadiumTimeFrame
        fields = ['time_frame', 'price']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'