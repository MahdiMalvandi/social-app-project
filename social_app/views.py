from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse
import random
from django.contrib.auth import logout, login
from .forms import *
from django.contrib.auth.decorators import login_required


# Create your views here.




def log_out(request):
    logout(request)
    return HttpResponse('you have logged out')


def homepage(request):
    return render(request, 'parent/base.html', {"user": request.user})


def register(request):
    if request.method == "POST":

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('social:home')
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {'form': form})


@login_required()
def ProfileEdit(request):
    if request.method == "POST":
        print(request.POST)
        user_form = EditUserForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect("social:home")
    else:
        user_form = EditUserForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'app/edit_profile.html', context)


@login_required()
def profile(request):
    user = request.user

    return HttpResponse(
        f'username => {user.username} full name => {user.first_name} {user.last_name} job => {user.job}')
