from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic

from .models import Question


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

