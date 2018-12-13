from django.urls import path
from . import views as v


urlpatterns = [
    # Forum
    path('<int:grouppk>/forum', v.redirectForum),
    path('<int:grouppk>/<slug:slug>/forum', v.GroupForumView.as_view(), name='forum'),
    path('<int:grouppk>/forum/new', v.redirectNewThread),
    # Thread
    path('<int:grouppk>/<slug:slug>/forum/new', v.GroupThreadCreate.as_view(), name='newthread'),
    path('<int:grouppk>/forum/<int:threadpk>', v.redirectViewThread),
    path('<int:grouppk>/forum/<int:threadpk>/<str:slug>', v.ThreadView.as_view(), name='viewthread'),
    path('post/<int:pk>', v.redirectPost),
    path('post/<int:pk>/edit', v.EditPostView.as_view(), name='editpost'),
    # Group
    path('create', v.CreateGroupView.as_view(), name='makegroup'),
    path('<int:pk>/', v.redirectGroup),
    path('<int:pk>/<slug:slug>', v.GroupHomepageView.as_view(), name='group-homepage'),
]
