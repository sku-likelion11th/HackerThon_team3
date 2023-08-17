from . import views
from django.urls import path

app_name = "service"
urlpatterns = [
    path('', views.main_page, name = "main_page"),
    path('service/', views.api_service_search, name = "api_service_search"),
    path('search_service/', views.search, name='search_service'),
]