from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Get questions and display them
# @login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list, 'page':'polls'}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
@login_required
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', { 'question': question })

# Get question and display results
# @login_required
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
@login_required
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))

@login_required
def resultsData(request, obj):
    votedata = []
    
    # question.choice_set.all is the queryset of choices which point to your question instance as the foreign key.
    #The default name for this inverse relationship is choice_set (because the related model is named Choice). But you can override this default name by specifying the related_name kwarg on the foreign key:
    
    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    return JsonResponse(votedata, safe=False)