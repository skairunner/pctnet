from django.urls import path
from django.contrib.auth.views import LoginView


urlpatterns = [
        path('', LoginView.as_view(template_name="login/login.html"), name='login'),
]

