from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse, JsonResponse
import random
from django.contrib.auth import logout, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, User, Following
from taggit.models import Tag
from django.db.models import Count


# Create your views here.


def log_out(request):
    logout(request)
    return HttpResponse('you have logged out')


def homepage(request):
    context = {
        "user": request.user,
        "saved_post": request.user.post_saved.all()
    }
    return render(request, 'parent/base.html', context)


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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('social:home')
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {'form': form})


@login_required()
def ProfileEdit(request):
    if request.method == "POST":
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
        posts = Post.objects.filter(tags__in=[tag]).order_by('-total_likes')
    else:
        posts = Post.objects.all()
        tag = None

    paginator = Paginator(posts, 1)
    page_number = page
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        last = posts.has_next()
        return render(request, 'partials/list-ajax.html', {'posts': posts, 'last': last})
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, "app/blog.html", context)


@login_required
def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.author = request.user

            form.save()
            form.save_m2m()
            PostsImage.objects.create(post=post, image=cd["image"])

            return redirect("social:posts")
    else:
        form = AddPostForm()
    context = {
        "form": form,
    }
    return render(request, "forms/addPostForm.html", context)


def detail_post(request, pk):
    """Get a post detail from pk

    :parameter:
        pk: int
            id of the post you want to show
    """
    post = get_object_or_404(Post, id=pk)
    posts_tag = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=posts_tag).exclude(id=pk)
    similar_posts = similar_post.annotate(same_posts=Count('tags')).order_by("-same_posts")
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'comments': comments,
        'is_login': request.user.is_authenticated

    }
    return render(request, 'app/detail.html', context)


def search_post(request):
    """ Get query and search into posts by tags and discription """
    query = ""
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results1 = Post.objects.annotate(similarity=TrigramSimilarity('discription', query)).filter(
                similarity__gt=0.1)

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
def add_comment(request, pk):
    """Add a comment to the Post

    :parameter :
        pk : int
            id of the post you want to add a comment to it
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Comments.objects.create(author=request.user, text=cd["text"], post_for=post)
            return redirect('social:detail', post.pk)
    else:
        form = CommentForm()

    return redirect('social:detail', pk)


@login_required
def delete_post(request, pk):
    """Delete a post from pk

    Parameters
    ----------
    pk : int
        id of the post you want to delete
    """
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('social:change_posts')


@login_required
def change_posts(request):
    """Return a HTML page"""
    return render(request, 'app/edit-buttons.html', {'posts': Post.objects.filter(author=request.user)})


@login_required
def edit_post(request, pk):
    """Edit a post from pk

    Parameters
    ----------
    pk : int
        id of the post you want to edit
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            PostsImage.objects.create(image=cd['image'], post=post)

            return redirect('social:change_posts')
    else:
        form = AddPostForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'forms/edit-posts.html', context)


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = Post.objects.select_related('author').get(id=post_id)
        user = request.user

        if user in post.likes.all():
            # unlike
            liked = False
            post.likes.remove(user)
        else:
            # like
            liked = True
            post.likes.add(user)

        post_likes_count = post.likes.count()

        response_data = {
            'liked': liked,
            'likes_count': post_likes_count
        }
    else:
        response_data = {
            'error': 'Invalid post_id'
        }
    return JsonResponse(response_data)


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.saved.all():
            # unsaved
            post.saved.remove(user)
            saved = False
        else:
            # saved
            post.saved.add(user)
            saved = True
        response_data = {
            'saved': saved
        }
    else:
        response_data = {
            'error': 'Invalid post_id'
        }
    return JsonResponse(response_data)


@login_required()
def get_all_users(request):
    all_users = User.objects.filter(is_active=True)
    return render(request, 'app/users-list.html', {'users': all_users})


@login_required()
def get_user_detail_by_username(request, username):
    user = get_object_or_404(User, is_active=True, username=username)
    return render(request, 'app/users-detail.html', {'user': user})


@login_required()
@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')
    if user_id is not None:
        user = get_object_or_404(User, is_active=True, id=user_id)
        try:
            if request.user in user.followers.all():
                # un follow
                Following.objects.filter(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                # follow
                Following.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True

            context = {
                'follow': follow,
                'total_followers': user.followers.count(),
                'total_following': user.following.count(),
            }
            return JsonResponse(context)
        except User.DoesNotExist:
            return JsonResponse({'error': 'the user does not exist'})
    else:
        return JsonResponse({'error': "Invalid request"})
