from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views
from chat.views import index

urlpatterns = [
    path('', index, name='home'),

    path('register/',views.register,name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout"),

]
