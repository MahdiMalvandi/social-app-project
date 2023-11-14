from rest_framework import serializers
from .models import Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = "__all__"

class PostAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
