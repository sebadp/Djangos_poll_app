from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.db.models import F 
from django.views import generic
from django.utils import timezone

# ANTES DE LAS GENERIC VIEWS
# def index(request):
#     latest_question_list= Question.objects.order_by('-pub_date')[:5] 
#     context= {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question= get_object_or_404(Question, pk=question_id)
#     return  render(request, 'polls/detail.html', {'question':question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Devolvemos las 5 Questions que fueron publicadas en el último día
        Pero no permitimos que muestren una asignada al futuro
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DateDetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excluye cualquier Question que no se haya publicado todavía
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionaste una opción.",
            })
    else:
        selected_choice.votes = F('votes') + 1  # acá evitamos el 'race condition' con F(): 
        selected_choice.save()                  # si dos votos suceden al mismo tiempo.
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
    
