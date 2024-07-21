from django.urls import path
from . import views

urlpatterns = [
    path("", views.ReviewCreateUpdateDeleteView.as_view()),
]
