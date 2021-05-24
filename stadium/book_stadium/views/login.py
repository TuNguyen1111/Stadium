from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import View

from book_stadium.myBackend import CustomAuthenticatedBackend
from book_stadium.models import Roles, Stadium

CustomAuthenticatedBackend = CustomAuthenticatedBackend()


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # REVIEW: ở đây không nên trực tiếp dùng CustomAuthenticatedBackend.authenticate,
        # mà nên dùng hàm authenticate import từ django.contrib.auth
        # Câu hỏi: Tại sao phải thế? (gợi ý: đọc thử code hàm authenticate của django)
        user = CustomAuthenticatedBackend.authenticate(
            request, username=email, password=password)

        if user:
            # REVIEW: ở đây không cần backend='book_stadium.myBackend.CustomAuthenticatedBackend'
            # TODO: cái này anh không chắc lắm nên chú kiểm tra xem đúng không
            login(request, user,
                  backend='book_stadium.myBackend.CustomAuthenticatedBackend')

            if user.role == Roles.OWNER:
                # REVIEW: đoạn này có thể viết hiệu quả hơn
                # Mình không cần tất cả các sân, chỉ cần sân đầu tiên
                # nên việc query nhiều sân xong kiểm tra len(stadiums) == 0 là không hiệu quả
                # Thay vào đó:
                # first_stadium = Stadium.objects.filter(owner=request.user).first()
                # if first_stadium:
                #   ...
                # else:
                #   ...
                #
                # Câu hỏi: viết như chú hiện tại thì mất 1 hay 2 câu query?
                # cụ thể: câu "len(stadiums) == 0" là mất 1 query rồi, sau đó viết
                # "fisrt_stadium = stadiums.first()" thì django có thực hiện 1 query nữa không?
                #
                # Gợi ý:
                # Set thứ tự sắp xếp mặc định của Stadium là id DESC (để khi .first() thì sẽ được Stadium tạo sau cùng)
                # Vào DB tạo Stadium xxx
                # Viết queryset "stadiums = Stadium.objects.all()"
                # Viết "len(stadiums)" để evaluate queryset này
                # Vào DB tạo thêm Stadium yyy
                # Viết "stadium = stadiums.first()" (.first() cho 1 queryset đã được evaluate)
                # Kiểm tra "stadium" là xxx hay yyy?
                stadiums = Stadium.objects.filter(owner=request.user)

                if len(stadiums) == 0:
                    return redirect('create_stadium')
                else:
                    fisrt_stadium = stadiums.first()
                    return redirect('owner', fisrt_stadium.pk)
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
        return redirect('home')
