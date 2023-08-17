from . import views
from django.urls import path

urlpatterns = [
    path('education/', views.api_education_search, name='education'),
]