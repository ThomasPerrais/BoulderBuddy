from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Problem


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def problems_by_gym(request, gym_abv):
    pbs = Problem.objects.filter(gym__abv = gym_abv)
    template = loader.get_template('gymstats/problems_list.html')
    context = {
        'problems_list': pbs,
    }
    return HttpResponse(template.render(context, request))

def problem_detail(request, id):
    try:
        pb = Problem.objects.get(id = id)
    except Problem.DoesNotExist:
        raise Http404("Problem does not exist")
    return render(request, 'gymstats/problem.html', {'problem': pb})