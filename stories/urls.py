from django.urls import path

from .views import ChapterDetailView, ChapterRedirect, StoryRedirect, StorySubmitView, StoryToChapterRedirect


urlpatterns = [
    # Chapters first due to URL routing
    path('chapter/<int:chapterpk>', ChapterRedirect, name='chapter-only-view'),
    path('<int:storypk>/chapter/<int:chapterpk>', ChapterRedirect),
    path('<int:storypk>/chapter/<int:chapterpk>/<str:slug>', ChapterDetailView.as_view(), name='viewchapter'),
    # Stories
    path('<int:pk>/', StoryRedirect),
    path('<int:pk>/<str:slug>/', StoryToChapterRedirect, name='viewstory'),
    path('submit/', StorySubmitView.as_view(), name='submitstory'),
]
