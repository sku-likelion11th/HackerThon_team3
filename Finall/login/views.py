from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import xml.etree.ElementTree as ET
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import AccessMixin
from post.models import Comment
from .models import User
from post.models import Post
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def main(request):
    return render(request, 'login/main/index.html')

def category(request):
    return render(request, 'login/Category/category.html')

def benefit(request):
    return render(request, 'service/Benefit.html')

def education(request):
    return render(request, 'education/education.html')

def consult(request):
    return render(request, 'post/Consult.html')


class RegisterView(UserPassesTestMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login/register.html"
    
    # UserPassesTestMixin 설정
    raise_exception = True
    test_func = lambda self: self.request.user.is_anonymous
    login_url = reverse_lazy('posts')
    redirect_field_name = None
    
    def handle_no_permission(self):
        messages.info(self.request, "이미 로그인한 사용자입니다.")
        return HttpResponseRedirect(reverse('post_list'))
    
    def get(self, request):
        serializer = RegisterSerializer()
        return render(request, "login/SignUp/Signup.html", {"serializer": serializer})

    def post(self, request):
        data = request.POST
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login/login/login.html"

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response({'serializer': serializer}, template_name=self.template_name)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['already_logged_in'] = True
            return HttpResponseRedirect(reverse_lazy('post_list')) 
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['token'] = token.key
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.error(request, "아이디와 비밀번호를 확인해주세요.")
            return self.get(request, *args, **kwargs)
        
    def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')  # 성공한 로그인 이후 리디렉션할 페이지
            else:
                return render(request, 'login.html', {'error_message': '잘못된 로그인 정보입니다.'})  # 오류 메시지를 context에 저장 후 리디렉션

        return render(request, 'login.html')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserUpdateView(LoginRequiredMixin, View): 
    model = User
    template_name = "login/MyPage/Mypage.html"

    def get(self, request):
        # 아래 코드로 게시물 및 댓글 목록을 가져옵니다.
        if not request.user.is_authenticated:
            messages.error(request, "로그인이 필요한 서비스입니다.")
            return HttpResponseRedirect(reverse_lazy("login"))
        else :
            user_posts = Post.objects.filter(author=request.user)
            user_comments = Comment.objects.filter(author=request.user)

            context = {
                'user_posts': user_posts,
                'user_comments': user_comments,
            }

            return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        user = authenticate(request, username=username, password=old_password)

        if user is not None and user.email.lower() == email.lower():
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "비밀번호 변경이 완료되었습니다.")
                logout(request)
                return HttpResponseRedirect(reverse_lazy("login"))
            else:
                messages.error(request, "새 비밀번호가 일치하지 않습니다.")
        else:
            messages.error(request, "아이디 또는 이메일이 잘못되었습니다.")

        return render(request, self.template_name)
    
    
class AnonymousRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("main"))  # 로그인한 사용자의 리디렉션 페이지 설정
        return super().dispatch(request, *args, **kwargs)
    
class PasswordResetView(AnonymousRequiredMixin, View): 
    template_name = "login/Password/Password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            user = None
            
        if user is not None:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                messages.success(request, "비밀번호 변경이 완료되었습니다.")
                return HttpResponseRedirect(reverse_lazy("login"))
            else:
                messages.error(request, "새 비밀번호가 일치하지 않습니다.")
        else:
            messages.error(request, "아이디 또는 이메일이 잘못되었습니다.")

        return render(request, self.template_name)