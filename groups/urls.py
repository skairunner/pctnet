from django.urls import path
from .views import CreateGroupView, GroupHomepageView, redirectGroup


urlpatterns = [
    path('create', CreateGroupView.as_view(), name='makegroup'),
    path('<int:pk>', redirectGroup),
    path('<int:pk>/<slug:slug>', GroupHomepageView.as_view(), name='group-homepage'),
]
