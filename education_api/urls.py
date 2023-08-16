from django.conf.urls import url
from . import views
from django.urls import path

app_name = "education_api"
urlpatterns = [
    path('', views.api_education_search, name = "api_education_search"),
    path('education_search/', views.search, name='education_search'),
    path('education_search/', views.search, name='search_education'),
]