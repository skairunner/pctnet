from django.urls import path

from .views import StoryDetailView


urlpatterns = [
    path('<int:pk>/', StoryDetailView.as_view()),
]
