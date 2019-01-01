from django.urls import path

from . import views as v

urlpatterns = [
    path('new', v.MakePMView.as_view(), name='makegroupmsg'),
    path('<int:pk>', v.PMView.as_view(), name='viewgroupmsg'),
]
