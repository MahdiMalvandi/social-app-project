from django.contrib import admin
from .models import User, Post
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('additional info', {'fields': ('date_of_birth', 'bio', 'photo', 'phone')}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["discription", "author"]