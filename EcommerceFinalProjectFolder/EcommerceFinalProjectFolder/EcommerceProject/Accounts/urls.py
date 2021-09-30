from django.urls import path
from .views import LoginView, RegisterView, SellerLoginView, SellerRegisterView, SellerShowView, ShowView, homeView



urlpatterns=[
    path('reg/',RegisterView,name='register'),
    path('log/',LoginView,name='login'),
    path('show/',ShowView,name='show'),
    path('sreg/',SellerRegisterView,name='sellerregister'),
    path('slog/',SellerLoginView,name='sellerlogin'),
    path('sshow/',SellerShowView,name='sellershow'),
    path('home/', homeView, name='home'),

]