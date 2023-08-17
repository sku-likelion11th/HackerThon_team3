from django.urls import path
from .views import (
    PostListViewHtml, PostDetailViewHtml, PostCreateViewHtml,
    CommentCreateView,
    PostUpdateViewHtml,
    CommentUpdateView,
)
from django.contrib.auth.views import LogoutView as DjangoLogoutView

urlpatterns = [
    path('posts/', PostListViewHtml.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailViewHtml.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post_create/', PostCreateViewHtml.as_view(), name='post_create'),
    path('post/<int:pk>/edit', PostUpdateViewHtml.as_view(), name='post_edit'),
    path('comment/<int:comment_id>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
]