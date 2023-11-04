from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.




class CommentInline(admin.TabularInline):
    """Tabular Inline View for Comment"""

    model = Comments
    extra = 0


class ImagesInline(admin.TabularInline):
    """Tabular Inline View for Comment"""

    model = PostsImage
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["discription", "author"]
    inlines = [
        CommentInline,
        ImagesInline
    ]