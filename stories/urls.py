from django.urls import path

from . import views as v


urlpatterns = [
    # Chapters first due to URL routing
    path('chapter/<int:chapterpk>', v.ChapterRedirect, name='chapter-only-view'),
    path('<int:storypk>/chapter/<int:chapterpk>', v.ChapterRedirect),
    path('<int:storypk>/chapter/<int:chapterpk>/<str:slug>', v.ChapterDetailView.as_view(), name='viewchapter'),
    # Comments
    path('comment/<int:pk>/delete', v.CommentDeleteView.as_view(), name='deletecomment'),
    path('comment/<int:pk>/edit', v.CommentEditView.as_view(), name='editcomment'),
    # Stories
    path('<int:pk>/', v.StoryRedirect),
    path('<int:pk>/<str:slug>/', v.StoryToChapterRedirect, name='viewstory'),
    path('submit/', v.StorySubmitView.as_view(), name='submitstory'),
]
