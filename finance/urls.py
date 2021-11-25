from django.urls import path , include # เชื่อม Project to App

from .views import finance

urlpatterns = [
    path('', finance),
]