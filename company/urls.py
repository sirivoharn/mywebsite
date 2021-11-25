from django.urls import path , include # เชื่อม Project to App

from .views import *

urlpatterns = [
    path('', Home, name='home-page'),
    path('about/', AboutUs, name='about-page' ),
    path('contact/', ContactUs, name='contact-page' ),
    path('accountant/', Accountant, name='accountant-page'),
    path('register/', Register, name='register-page'),
    path('profile/', ProfilePage, name='profile-page'),
    path('reset-password/', ResetPassword, name='resetpassword-page'),
    path('reset-new-password/<str:token>/', ResetNewPassword, name='reset-newpassword-page'),
    path('verify-email/<str:token>/', Verify_Success, name='verifyemail-page'),
    path('action-detial/<int:cid>', ActionPage, name='action-page'),
    path('add-product/', AddProduct, name='addproduct-page'),
]
