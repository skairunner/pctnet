from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignupView


urlpatterns = [
    path('', LoginView.as_view(template_name="login/login.html"), name='login'),
    path('signup', SignupView, name='signup'),
]

