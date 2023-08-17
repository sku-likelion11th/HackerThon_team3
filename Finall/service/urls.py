from . import views
from django.urls import path

urlpatterns = [
    path('service/', views.api_service_search, name = "service"),
]