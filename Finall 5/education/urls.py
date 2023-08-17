from . import views
from django.urls import path

urlpatterns = [
    path('education/', views.api_education_search, name = "education"),
    path('education_search/', views.search, name='education_search'),
]