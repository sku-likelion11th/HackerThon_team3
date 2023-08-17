from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import Post, Comment, Category
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import serializers, exceptions
  
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name') 
  
class PostSerializer(serializers.ModelSerializer):
  category = CategorySerializer(many=True, read_only=True)
  class Meta:
    model = Post
    fields = ('id', 'title', 'content', 'author', 'created_at', 'category')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post','created_at')