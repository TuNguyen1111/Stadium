from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('owner/', views.OwnerPage.as_view(), name='owner'),
    path('register/', views.Register.as_view(), name='register'),
]
