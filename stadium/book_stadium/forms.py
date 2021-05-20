from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Stadium, StadiumTimeFrame
from crispy_forms.helper import FormHelper
from django.contrib.auth.hashers import make_password
from .models import User, Stadium, StadiumTimeFrame, TimeFrame, Order, StarRating
from django.contrib import messages
from django.core.exceptions import ValidationError
from random import choice


class UserCreationForm(UserCreationForm):
    # đống này để set custom cho Register form nha
    email_or_phone = forms.CharField(
        label="Email hoặc số điện thoại", max_length=254)
    password1 = forms.CharField(
        label="Mật khẩu", widget=forms.PasswordInput,
        help_text="""
        Mật khẩu không chứa thông tin cá nhân <br>
        Mật khẩu phải lớn hơn 8 ký tự <br>
        Mật khẩu gồm ít nhất 1 chữ hoa, 1 chữ thường, 1 số, 1 ký tự đặc biệt
        """
    )
    password2 = forms.CharField(
        label="Nhập lại mật khẩu", widget=forms.PasswordInput,
        help_text=""
    )

    class Meta:
        model = User
        fields = ['role', 'email_or_phone', 'password1', 'password2']
        labels = {
            'role': 'Bạn là',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            email_or_phone = self.cleaned_data.get('email_or_phone')
            password = self.cleaned_data.get('password1')
            password = make_password(password)
            role = self.cleaned_data.get('role')

            if '@' in email_or_phone:
                user = User.objects.create(
                    email=email_or_phone,
                    password=password,
                    role=role
                )
            else:
                user = User.objects.create(
                    phone_number=email_or_phone,
                    password=password,
                    role=role
                )
            user.save()
        return user

    def clean_email_or_phone(self):
        user = self.cleaned_data['email_or_phone']
        if '@' in user:
            user_data = User.objects.filter(email=user)
        else:
            user_data = User.objects.filter(phone_number=user)
        if user_data:
            raise forms.ValidationError('Tên tài khoản của bạn đã tồn tại!')
        return user


class OrderForm(forms.ModelForm):
    stadium_name = forms.CharField(label="Tên sân", max_length=100, widget=forms.TextInput(
        attrs={'id': 'stadium-name', 'readonly': True}))
    time_frame = forms.ModelChoiceField(label="Khung giờ", queryset=TimeFrame.objects.all(
    ), widget=forms.Select(attrs={'id': 'time_frame'}))

    class Meta:
        model = Order
        fields = ['stadium_name', 'order_date', 'time_frame', 'pitch_clothes',
                  'type_stadium', 'customer_name', 'customer_phone_number']
        labels = {
            'order_date': 'Ngày đặt',
            'customer_phone_number': 'Số điện thoại',
            'customer_name': 'Tên người đặt',
            'pitch_clothes': 'Áo pitch',
            'type_stadium': 'Loại sân'
        }

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            stadium_name = self.cleaned_data.get('stadium_name')
            order_date = self.cleaned_data.get('order_date')
            time_frame = self.cleaned_data.get('time_frame')
            pitch_clothes = self.cleaned_data.get('pitch_clothes')
            type_stadium = self.cleaned_data.get('type_stadium')
            customer_name = self.cleaned_data.get('customer_name')
            customer_phone_number = self.cleaned_data.get(
                'customer_phone_number')
            stadium_timeframe = StadiumTimeFrame.objects.get(
                time_frame=time_frame, stadium__name=stadium_name)
            order = Order.objects.create(order_date=order_date, stadium_time_frame=stadium_timeframe, pitch_clothes=pitch_clothes,
                                         type_stadium=type_stadium, customer_phone_number=customer_phone_number, customer_name=customer_name)
            order.save()
        return order

    def clean(self):
        time_frame = self.cleaned_data.get('time_frame')
        stadium_name = self.cleaned_data.get('stadium_name')
        order_date = self.cleaned_data.get('order_date')
        type_stadium = self.cleaned_data.get('type_stadium')
        stadium_timeframe = StadiumTimeFrame.objects.get(
            time_frame=time_frame, stadium__name=stadium_name)
        stadium_of_timeframe_field_count = stadium_timeframe.stadium.field_count
        orders = Order.objects.filter(
            stadium_time_frame=stadium_timeframe, order_date=order_date, is_accepted=True)
        all_fields = list(range(1, stadium_of_timeframe_field_count + 1))
        for order in orders:
            if order.type_stadium == '7players':
                field_number_accepted = order.field_numbers
                if field_number_accepted in all_fields:
                    all_fields.remove(field_number_accepted)
            else:
                for number_of_field in order.field_numbers:
                    if number_of_field in all_fields:
                        all_fields.remove(number_of_field)
        if type_stadium == '11players':
            if len(all_fields) < 3:
                raise forms.ValidationError(
                    'Khung giờ của này không đủ để chuẩn bị sân 11! Vui lòng chọn khung giờ khác!')
        else:
            if not all_fields:
                raise forms.ValidationError(
                    'Khung giờ của này đã hết sân! Vui lòng chọn khung giờ khác!')
        return self.cleaned_data


class StadiumForm(forms.ModelForm):
    # sửa lại class form theo kiểu t quen. M thích thì sửa lại như cũ cũng đc
    # viết thế này để t check có instance truyền vào không. Do dùng chung form để add với edit
    def __init__(self, *args, **kwargs):
        super(StadiumForm, self).__init__(*args, **kwargs)
        # check xem có truyền instance vào không
        self._newly_created = kwargs.get('instance')
        # cái này để set input cho ảnh trông đỡ xấu, xoá thử đi để trải nghiệm nếu muốn
        self.fields['image'] = forms.FileField(
            label='Ảnh', widget=forms.FileInput)
        # update input ảnh tự động tìm ảnh. Sau phải validate lại bằng JS đấy
        self.fields['image'].widget.attrs.update({
            'accept': '.png, .jpg, .jpeg"'
        })
        # nếu mà có instance thì disable input
        if self._newly_created:
            for name in self.fields.keys():
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                    'disabled': True
                })
        else:
            for name in self.fields.keys():
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                })
        # ẩn trường owner trong form đi.
        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    class Meta:
        model = Stadium
        fields = ['name', 'address', 'field_count', 'image', 'owner']
        labels = {
            'name': 'Tên sân',
            'address': 'Địa chỉ',
            'field_count': 'Số sân có thể đặt',
            'image': 'Ảnh sân',
            'owner': ''
        }


class StadiumFormForUser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StadiumFormForUser, self).__init__(*args, **kwargs)
        self._newly_created = kwargs.get('instance')
        if self._newly_created:
            for name in self.fields.keys():
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                    'disabled': True
                })
        else:
            for name in self.fields.keys():
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                })
        # ẩn trường owner trong form đi.
        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    class Meta:
        model = Stadium
        fields = ['name', 'address', 'field_count', 'owner']
        labels = {
            'name': 'Tên sân',
            'address': 'Địa chỉ',
            'field_count': 'Số sân có thể đặt',
            'owner': ''
        }


class StadiumTimeFrameForm(forms.ModelForm):
    time_frame = forms.ModelChoiceField(
        queryset=TimeFrame.objects.all(), disabled=True)

    class Meta:
        model = StadiumTimeFrame
        fields = ['time_frame', 'price', 'is_open']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email']
        labels = {
            'username': 'Tên người dùng',
            'phone_number': 'Số điện thoại',
            'email': 'Email'
        }


class ChangeNumberOfStadium7Form(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    stadium_type = forms.CharField(widget=forms.HiddenInput(
        attrs={'value': '7players'}), required=False)
    field_number = forms.IntegerField(
        label='Nhập vị trí sân: ', widget=forms.NumberInput(attrs={'class': 'field_number'}))

    def save(self):
        order_id = self.cleaned_data.get('order_id')
        field_number = self.cleaned_data.get('field_number')

        order = Order.objects.get(id=order_id)
        order.field_numbers = field_number
        order.save()
        return order


class ChangeNumberOfStadium11Form(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    stadium_type = forms.CharField(widget=forms.HiddenInput(
        attrs={'value': '11players'}), required=False)
    field_1 = forms.IntegerField(label='Nhập vị trí sân thứ nhất: ',
                                 widget=forms.NumberInput(attrs={'class': 'field_number'}))
    field_2 = forms.IntegerField(label='Nhập vị trí sân thứ hai: ',
                                 widget=forms.NumberInput(attrs={'class': 'field_number'}))
    field_3 = forms.IntegerField(label='Nhập vị trí sân thứ ba: ', widget=forms.NumberInput(
        attrs={'class': 'field_number'}))

    def save(self):
        order_id = self.cleaned_data.get('order_id')
        field_1 = self.cleaned_data.get('field_1')
        field_2 = self.cleaned_data.get('field_2')
        field_3 = self.cleaned_data.get('field_3')

        order = Order.objects.get(id=order_id)
        field = [field_1, field_2, field_3]
        order.field_numbers = field
        order.save()
        return order


class StarRatingForm(forms.ModelForm):
    class Meta:
        model = StarRating
        fields = ['comment']
        labels = {
            'comment': 'Bình luận'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'id': 'comment-input'}),
        }
