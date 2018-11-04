from django.urls import path

from .views import StoryDetailView, StoryRedirect, StorySubmitView


urlpatterns = [
    path('<int:pk>/', StoryRedirect),
    path('<int:pk>/<str:slug>/', StoryDetailView.as_view(), name='viewstory'),
    path('submit/', StorySubmitView.as_view(), name='submitstory'),
]
