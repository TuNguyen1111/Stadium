from django.urls import path, include
# check lại chỗ này để hiện ảnh nhé. Có gì hỏi a Trung vụ hiện ảnh từ db ra xem ntn.
# cái này là t đi cop về được
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from .views import isAccepted
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('owner/', views.OwnerPage.as_view(), name='owner'),
    path('register/', views.Register.as_view(), name='register'),
    path('them-san/', views.CreateStadium.as_view(), name='create_stadium'),
    path('chi-tiet-san/<int:pk>', views.StadiumDetail.as_view(), name='stadium_detail'),
    path('accepted/<int:id>', views.isAccepted, name='accepted'),
    path('trang-ca-nhan/<int:id>', views.UserProfile.as_view(), name='user_profile'),
]
# đống này nữa
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# với trong settings.py nữa