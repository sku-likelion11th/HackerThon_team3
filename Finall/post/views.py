from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import xml.etree.ElementTree as ET
from .models import Post, Comment, Category, Category2
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q

class PostListViewHtml(generic.ListView):     
    model = Post     
    template_name = 'post/Consult.html'          
    
    def get_queryset(self):         
        query = self.request.GET.get('q')         
        category1 = self.request.GET.get('category1')         
        category2 = self.request.GET.get('category2')         
        qs = Post.objects.all()          
        if query:             
            qs = qs.filter(Q(title__icontains=query))          
            
        if category1:             
            cat1 = Category.objects.get(pk=int(category1))  # id 값으로 변경
            qs = qs.filter(categories=cat1)          

        if category2:              
            cat2 = Category2.objects.get(pk=int(category2))  # id 값으로 변경
            qs = qs.filter(categories2=cat2)          
            
        return qs

class PostDetailViewHtml(generic.DetailView):
    model = Post
    template_name = 'post/Consult_Content.html'

class PostCreateViewHtml(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'post/Consult_Write.html'
    fields = ('title', 'content', 'categories', 'categories2')  # 수정된 부분: categories2 추가
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        categories = self.request.POST.getlist('category')
        for category in categories:
            self.object.categories.add(Category.objects.get(id=int(category)))

        categories2 = self.request.POST.getlist('category2')  # 수정된 부분: Category_2를 Category2로 수정
        for category2 in categories2:
            self.object.categories2.add(Category2.objects.get(id=int(category2))) # 수정된 부분: Category_2를 Category2로 수정

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['categories2'] = Category2.objects.all()  # 추가된 부분: categories2를 컨텍스트에 추가
        return context

    def handle_no_permission(self):
        messages.warning(self.request, "로그인이 필요한 서비스입니다.")  
        return super().handle_no_permission()
    
    def get_success_url(self):
        return reverse_lazy('post_list')
    
class PostUpdateViewHtml(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'post/Consult_Write.html'
    fields = ('title', 'content', 'categories')
    login_url = '/login/'

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            messages.warning(self.request, "본인이 작성한 글만 수정할 수 있습니다.")
            return HttpResponseRedirect(self.get_success_url())

        response = super().form_valid(form)
        categories = self.request.POST.getlist('categories')
        form.instance.categories.clear()
        for category_id in categories:
            category = Category.objects.get(pk=category_id)
            self.object.categories.add(category)
            
        return response

    def handle_no_permission(self):
        messages.warning(self.request, "로그인이 필요한 서비스입니다.")
        return super().handle_no_permission()
    
    def get_success_url(self):
        return reverse_lazy('post_list')
    
    def get(self, request):
        messages.set_level(request, messages.ERROR)  # 메시지 초기화 코드
        return render(request, self.template_name)

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ('content',)
    login_url = '/login/' 

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        self.object = form.save()  # 댓글을 데이터베이스에 저장
        return HttpResponseRedirect(self.get_success_url())
    
    def handle_no_permission(self):
        messages.warning(self.request, "로그인이 필요한 서비스입니다.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
    
class CommentUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user != comment.author:
            messages.warning(request, "본인이 작성한 댓글만 수정할 수 있습니다.")
            return redirect('post_detail', pk=comment.post.pk)

        content = request.POST.get('content', '')
        if content:
            comment.content = content
            comment.save()
            messages.success(request, '댓글이 수정되었습니다.')
            return redirect('post_detail', pk=comment.post.pk)
        else:
            messages.warning(request, '댓글 수정에 실패했습니다.')
            return redirect('post_detail', pk=comment.post.pk)

    def handle_no_permission(self):
        messages.warning(self.request, "로그인이 필요한 서비스입니다.")
        return super().handle_no_permission()