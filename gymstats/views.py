from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Problem, Gym, Review, Climber


# Create your views here.

def index(request):
    # Main page: explore gyms, explore problems, explore sessions, ... -> put in a side menu 
    return HttpResponse("Hello, world. You're at the gymstats index.")


# GYM views

def gyms_homepage(request):
    gyms = Gym.objects.all()
    return render(request, 'gymstats/list.html', {'list': gyms})  # TODO: change the display


def gym_details(request, gym_abv):
    gym = get_object_or_404(Gym, abv=gym_abv)
    # TODO display infos
    return render(request, 'gymstats/gym.html', {'gym': gym})


def problems_by_gym(request, gym_abv):
    pbs = Problem.objects.filter(gym__abv = gym_abv)
    return render(request, 'gymstats/problems_list.html', {'problems_list': pbs})


# PROBLEM views

def problems_homepage(request):
    pbs = Problem.objects.all()
    return render(request, 'gymstats/problems_list.html', {'problems_list': pbs})


def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'gymstats/problem.html', {'problem': problem})


def problem_reviews(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    reviews = problem.review_set.all()
    return render(request, 'gymstats/reviews_list.html', {'problem': problem, 'reviews_list': reviews})


def problem_review(request, problem_id, review_id):
    problem = get_object_or_404(Problem, id=problem_id)
    try:
        review = problem.review_set.get(id=review_id)
    except Review.DoesNotExist:
        raise Http404("Review does not exist")
    return render(request, 'gymstats/review.html', {'review': review})


def review_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    try:
        # get comment from POST
        comment = request.POST['comment']
        climber = get_object_or_404(Climber, name="Thomas")  # TODO: retrieve logged in Climber
        rating = int(request.POST["rating"])
    except KeyError:
        return render(request, 'gymstats/problem.html', {
            'problem': problem,
            'error_message': "Error while handling comment - try again",
        })
    else:
        r = Review(reviewer=climber, comment=comment, problem=problem, rating=rating)
        r.save()
        return HttpResponseRedirect(reverse('gs:pb-review-display', args=(problem.id, r.id,)))
