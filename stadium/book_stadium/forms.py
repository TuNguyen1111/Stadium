from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Stadium, StadiumTimeFrame
from crispy_forms.helper import FormHelper

class UserCreationForm(UserCreationForm):
    # đống này để set custom cho Register form nha
    email_or_phone = forms.CharField(label="Email hoặc số điện thoại",max_length=254)
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
    # sửa lại class form theo kiểu t quen. M thích thì sửa lại như cũ cũng đc
    # viết thế này để t check có instance truyền vào không. Do dùng chung form để add với edit
    def __init__(self, *args, **kwargs):
        super(StadiumForm, self).__init__(*args, **kwargs)
        # check xem có truyền instance vào không
        self._newly_created = kwargs.get('instance')
        # cái này để set input cho ảnh trông đỡ xấu, xoá thử đi để trải nghiệm nếu muốn
        self.fields['image'] = forms.FileField(widget=forms.FileInput)
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


class StadiumTimeFrameForm(forms.Form):
    class Meta:
        model = StadiumTimeFrame
        fields = ['time_frame', 'price']

       


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'