from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "social"

urlpatterns = [

    # login or log out
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),
]

