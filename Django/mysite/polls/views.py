from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    """
    View that is loaded when requesting index page '/'
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    View that gets details of a specific question
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes questions that are still now published
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes questions that are still now published
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

    """
    def index(request):
        question_list = Question.objects.order_by('-pub_date')[:5]
        context = {
            'question_list': question_list,
        }
        return render(request, 'polls/index.html', context)


    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        # Is the same as
        # try:
        #    question = Question.objects.get(pk=question_id)
        # except Question.DoesNotExist:
        #    raise Http404("Question does not exsist")
        return render(request, 'polls/detail.html', {'question': question})


    def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(
            request,
            'polls/results.html',
            {
                'question': question
            }
        )
    """


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choise",
            }
        )
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
