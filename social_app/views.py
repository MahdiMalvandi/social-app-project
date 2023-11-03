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
from django.db.models import Count

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
            send_mail(cd['title'], email_message, 'mahdimalvandi6@gmail.com',
                      ['zohrezahedi1981@gmail.com', 'mahdimll1386@gmail.com'],
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
            login(request, user)
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


@login_required
def add_post(request):
    context = {}
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            form.save_m2m()
            return redirect("social:posts")
    else:
        form = AddPostForm()
    context = {
        "form": form,
    }
    return render(request, "forms/addPostForm.html", context)


def detail_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    posts_tag = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=posts_tag).exclude(id=pk)
    similar_posts = similar_post.annotate(same_posts=Count('tags')).order_by("-same_posts")
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'comments': comments

    }
    return render(request, 'app/detail.html', context)


def search_post(request):
    """ Get query and search into posts by tags and discription"""
    query = ""
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results1 = Post.objects.annotate(similarity=TrigramSimilarity('discription', query)).filter(similarity__gt=0.1)

            # get similar tags
            similar_tags = Post.tags.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.1)

            # get similar posts by similar tags
            similar_post = Post.objects.filter(tags__in=similar_tags)

            # order similar posts by same tags
            results2 = similar_post.annotate(same_posts=Count('tags')).order_by("-same_posts")
            results = (results1 | results2).order_by("-similarity")
            results = results.annotate(same_posts=Count('tags')).order_by("-same_posts")

    context = {
        'posts': results,
        'query': query
    }
    return render(request, 'app/blog.html', context)


@login_required()
def add_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Comments.objects.create(author=request.user, text=cd["text"], post_for=post)
            return redirect('social:detail', post)
    else:
        form = CommentForm()
    return redirect('social:detail', post)
