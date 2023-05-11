from datetime import date
import math
from collections import defaultdict
import itertools

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Problem, Gym, Review, Climber, Session, Try


# Create your views here.

def index(request):
    # Main page: explore gyms, explore problems, explore sessions, ... -> put in a side menu 
    return HttpResponse("Hello, world. You're at the gymstats index.")

# Homepage view

def home(request):
    sessions = {elt.date.strftime("%d/%m/%Y"): elt.id for elt in Session.objects.only("date")}
    return render(request, 'gymstats/home.html', {'sessions': sessions})


# Profil view

def profil(request):
    data = {}
    return render(request, 'gymstats/profil.html', {'data': data})



# Session views

def session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    sess_data = __session_stats(session)
    return render(request, 'gymstats/session.html', {'session': session, 'sess_data': sess_data})


def __session_stats(session: Session):
    
    ## general data
        # percentage of successes
    tops = session.tops.count()
    fails = session.failures.count() + session.zones.count()
    total = tops + fails
    successes = math.floor(tops * 100/ total) if total > 0 else "??"

    # problems specific data
        # types, grades, holds
    pb_types = defaultdict(lambda: [0,0])
    pb_grades = defaultdict(lambda: [0,0])
    if session.gym.brand == "Block'Out":  # needed to order correctly, TODO: handle this elsewhere
        pb_grades = { 'B' + str(i): [0,0] for i in range(14) }
    pb_holds = defaultdict(lambda: [0,0])

    def _add(t: Try, pos: int):
        pb_types[str(t.problem.problem_type)][pos] += 1
        pb_grades[str(t.problem.grade)][pos] += 1
        for hh in t.problem.hand_holds.all():
            pb_holds[str(hh)][pos] += 1

    for t in session.tops.all():
        _add(t, 0)
    for t in itertools.chain(session.failures.all(), session.zones.all()):
        _add(t, 1)

    pb_grades = { k: v for k,v in pb_grades.items() if sum(v) > 0 }

    data = {
        # general data
        "duration": session.duration,
        "grade": session.overall_grade,
        "successes": successes,

        # pb specific
        'problems': {
            'types': pb_types,
            'grades': pb_grades,
            'holds': pb_holds
        }
    }
    return data


def session_statistics(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return JsonResponse(data=__session_stats(session))


def session_details(request, session_id):
    session = get_object_or_404(Session, abv=session_id)
    # TODO display infos
    return render(request, 'gymstats/session_details.html', {'session': session})


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
