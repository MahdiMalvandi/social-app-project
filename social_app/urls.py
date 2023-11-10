from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "social"

urlpatterns = [
    # pages
    path('', views.homepage, name='home'),
    path("contactUs/", views.ticket, name="contact_us"),
    path('posts/', views.post_list, name="posts"),
    path('posts/tag/<str:tag_slug>', views.post_list, name="get_posts_tag"),
    path('profile/', views.profile, name="profile"),
    path('posts/detail/<pk>/', views.detail_post, name="detail"),
    path('posts/page/<str:page>/', views.post_list, name="posts by page"),
    path('posts/page/<str:tag_slug>/<str:page>/', views.post_list, name="posts by page and tag"),
    path('posts/edit-and-delete/', views.change_posts, name="change_posts"),

    # login or log out
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),

    # sign up
    path('register/', views.register, name="register"),
    path('user/edit/', views.ProfileEdit, name="ProfileEdit"),

    # forms
    path('posts/create_post/', views.add_post, name="Add New Post"),
    path('search/', views.search_post, name="search post"),
    path('add-post/<pk>/', views.add_post, name="Add New Post"),
    path('add-comments/<pk>/', views.add_comment, name="add comment"),

    # Edit And Delete Posts
    path('posts/edit/<pk>/', views.edit_post, name='edit post'),
    path('posts/delete/<pk>/', views.delete_post, name='delete post'),

    # like post
    path('like-post/', views.like_post, name='like post'),

    # save and un save
    path('posts/save/', views.save_post, name='save post'),

    # get users ot user detail
    path('users/', views.get_all_users, name='get all users'),
    path('users/<username>', views.get_user_detail_by_username, name="get user detail by username"),

     # follow
    path('follow/', views.follow_user, name='follow user'),
]

