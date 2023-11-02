from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse
import random
from django.contrib.auth import logout, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Post, User
from taggit.models import Tag


# Create your views here.


def log_out(request):
    logout(request)
    return HttpResponse('you have logged out')


def homepage(request):
    return render(request, 'parent/base.html', {"user": request.user})


def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            email_message = f'You Have a message from {user.first_name} {user.last_name} ' \
                            f'message title is {cd["title"]}' \
                            f'message is:' \
                            f' {cd["message"]}'
            send_mail(cd['title'], email_message, 'mahdimalvandi6@gmail.com', ['zohrezahedi1981@gmail.com', 'mahdimll1386@gmail.com'],
                      fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    return render(request, "app/contactus.html", {"form": form, 'sent': sent})


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


def post_list(request, tag_slug=None, page=1):
    if tag_slug is not None:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag]).order_by('-created')
    else:
        posts = Post.objects.all()
        tag = None

    # paginator = Paginator(posts, 12)
    # page_number = page
    # try:
    #     posts = paginator.page(page_number)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, "app/blog.html", context)
