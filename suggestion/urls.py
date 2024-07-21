from django.urls import path
from . import views

urlpatterns = [
    path("", views.SuggestionView.as_view()),
]
