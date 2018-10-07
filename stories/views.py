from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Story


class StoryDetailView(DetailView):
    model = Story
