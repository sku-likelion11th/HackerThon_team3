from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserUpdateView,
    PasswordResetView,
)
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from .import views
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path("", LoginView.as_view(), name="login"),
    path('logout/', DjangoLogoutView.as_view(), name='logout'),
    path("mypage/", UserUpdateView.as_view(), name="mypage"),
    path('password/', PasswordResetView.as_view(), name='password'),
    path('main/', views.main, name='main'),
    path('category/', views.category, name='category'),
    path('benefit/', views.benefit, name='benefit'),
    path('consult/', views.consult, name='consult'),
]