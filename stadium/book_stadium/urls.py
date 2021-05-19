from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('owner/<int:pk>', views.OwnerPage.as_view(), name='owner'),
    path('register/', views.Register.as_view(), name='register'),
    path('them-san/', views.CreateStadium.as_view(), name='create_stadium'),
    path('chi-tiet-san/<int:pk>',
         views.StadiumDetail.as_view(), name='stadium_detail'),
    path('accepted/<int:pk>', views.AcceptOrderView.as_view(), name='accepted'),
    path('trang-ca-nhan/<int:pk>', views.UserProfile.as_view(), name='user_profile'),
    path('', views.BookStadium.as_view(), name='book_stadium'),
    path('lich-su-dat-san/<int:pk>',
         views.HistoryBookedOfUser.as_view(), name="history_booked"),
    path('tim-kiem-san/', views.SearchStadium.as_view(), name="search_stadium"),
    path('thay-doi-vi-tri-san/<int:pk>',
         views.ChangeNumberOfField.as_view(), name='field_number_change'),

    path('thay-doi-mat-khau/', views.PasswordChange.as_view(),
         name='password_change'),

    path('reset-mat-khau/', auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset.html'), name='reset_password'),
    path('reset-mat-khau-tin-nhan/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-mat-khau-thanh-cong/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_done.html'), name='password_reset_complete'),

    path('thong-bao/', views.Notifications.as_view(), name='notifications'),
    path('chi-tiet-thong-bao/<int:pk>',
         views.NotificationDetail.as_view(), name='notification_detail'),
    path('doanh-thu/<int:pk>', views.OwnerProfit.as_view(), name='owner_profit'),
    path('danh-gia/', views.StadiumRating.as_view(), name='stadium_rating'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
