from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_page, name = "main_page"),
    path('service/', views.api_service_search, name = "service"),
    path('search_service/', views.search, name='search_service'),
]