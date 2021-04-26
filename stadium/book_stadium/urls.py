from django.urls import path, include

from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
     path('social-auth/', include('social_django.urls', namespace="social")),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('owner/<int:id>', views.OwnerPage.as_view(), name='owner'),
    path('register/', views.Register.as_view(), name='register'),
    path('them-san/', views.CreateStadium.as_view(), name='create_stadium'),
    path('chi-tiet-san/<int:pk>', views.StadiumDetail.as_view(), name='stadium_detail'),
    path('accepted/<int:id>', views.isAccepted.as_view(), name='accepted'),
    path('trang-ca-nhan/<int:id>', views.UserProfile.as_view(), name='user_profile'),
    path('dat-san/', views.BookStadium.as_view(), name='book_stadium'),
    path('lich-su-dat-san/<int:id>', views.HistoryBookedOfUser.as_view(), name="history_booked")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


