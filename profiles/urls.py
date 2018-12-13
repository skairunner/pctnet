from django.urls import path

from .views import CurrentUserRedirect, UserProfileView, UserRedirect, ProfileUpdateView


urlpatterns = [
    path('', CurrentUserRedirect),
    path('<int:pk>/', UserRedirect),
    path('<int:pk>/<str:slug>/', UserProfileView.as_view(), name='viewuser'),
    path('update/<int:pk>/', ProfileUpdateView.as_view(), name='updatebio'),
]
