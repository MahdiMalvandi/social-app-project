from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "social"

urlpatterns = [
    path('', views.homepage, name='home'),
    path("contactUs/", views.ticket, name="contact_us"),

    # login or log out
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),

    # sign up
    path('register/', views.register, name="register"),
    path('user/edit/', views.ProfileEdit, name="ProfileEdit"),

    path('profile/', views.profile, name="profile"),
]

