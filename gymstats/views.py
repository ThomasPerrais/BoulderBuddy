from collections import defaultdict
from datetime import date
import itertools
import math
import re

from dal import autocomplete

from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils.html import format_html

from .forms import SessionForm
from .models import Problem, Gym, Review, Climber, Session, Try, RIC, Sector
from .helper.parser import parse_filters
from .helper.query import query_problems_from_filters
from .helper.grade_order import BRAND_TO_ABV, GRADE_ORDER

# Create your views here.

# AutoComplete views

class GymAutocompleteView(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        gyms = Gym.objects.all()
        if self.q:
            gyms = gyms.filter(abv__startswith=self.q)
        return gyms

class SectorAutocompleteView(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):

        sectors = Sector.objects.all()

        gym = self.forwarded.get('gym', None)
        if gym:
            sectors = sectors.filter(gym__id=gym)

        if self.q:
            sectors = sectors.filter(gym__abv__startswith=self.q)
        return sectors

class ProblemAutocompleteView(autocomplete.Select2QuerySetView):

    re_num = re.compile("^(\d+)(.*)")

    def get_queryset(self):
        problems = Problem.objects.all()

        # Forwarded in Session Form
        gym = self.forwarded.get('gym', None)
        if gym:
            problems = problems.filter(gym__id=gym)
        
        sector = self.forwarded.get('sector', None)
        if sector:
            problems = problems.filter(sector__id=sector)
        
        # Forwarded in Try Form --> TODO: why is it not working???
        sess_id = self.forwarded.get('session', None)
        if sess_id:
            gym_id = Session.objects.get(id=sess_id).gym.id
            problems = problems.filter(gym__id=gym_id)

        if self.q:
            m = self.re_num.search(self.q)
            if m:
                sector = m.group(1)
                grade = m.group(2)
                problems = problems.filter(sector__sector_id=int(sector))
            else:
                grade = self.q
            problems = problems.filter(grade__startswith=grade)
        return problems


class GradeAutocompleteView(autocomplete.Select2ListView):

    def get_list(self):

        grades = []
        gym = self.forwarded.get('gym', None)
        if gym:
            gym_brand = Gym.objects.get(id=gym).brand
            if gym_brand in BRAND_TO_ABV:
                grades = GRADE_ORDER[BRAND_TO_ABV[gym_brand]]
            else:
                grades = GRADE_ORDER["@default"]
            grades = [elt[0].upper() + elt[1:] for elt in grades]

        return grades


def index(request):
    # Main page: explore gyms, explore problems, explore sessions, ... -> put in a side menu 
    return HttpResponse("Hello, world. You're at the gymstats index.")

# Homepage view

def home(request):
    sessions = {elt.date.strftime("%d/%m/%Y"): (elt.id,) for elt in Session.objects.only("date")}
    return render(request, 'gymstats/home.html', {'sessions': sessions})


# Profil view

def profil(request):
    data = {}
    return render(request, 'gymstats/profil.html', {'data': data})



# Session views

def new_session(request):
    form = SessionForm();
    return render(request, 'gymstats/new_session.html', {"session_form": form})


def add_session(request):
    try:
        # get comment from POST
        comment = request.POST['comment']
        climber = get_object_or_404(Climber, name="Thomas")  # TODO: retrieve logged in Climber
        rating = int(request.POST["rating"])
    except KeyError:
        return render(request, 'gymstats/new_session.html', {
            'error_message': "Error while adding session, try again",
        })
    else:
        s = Session()
        s.save()
        return HttpResponseRedirect(reverse('gs:session-add-problems', args=(s.id,)))

    


def add_session_problems(request):
    return render(request, 'gymstats/add_session_problems.html')



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
    filters = {"gym": gym_abv}
    return render(request, 'gymstats/problem_results.html', {'results': pbs, 'filters': filters})


# PROBLEM views

def problems_homepage(request):
    pbs = Problem.objects.all()
    return render(request, 'gymstats/problems_list.html', {'problems_list': pbs})


def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    # Problem data: rating & RIC
    ratings = problem.review_set.all()
    if len(ratings) > 0:
        avg_rating = sum([r.rating for r in ratings]) / len(ratings)
    else:
        avg_rating = "NA"
    
    rics = problem.ric_set.all()
    if len(rics) > 0:
        avg_ric = sum([r.average() for r in rics]) / len(rics)
    else:
        avg_ric = "NA"

    # Sessions where problem was tried
    only = ["session__date", "session__id"]
    status = "Not Tried";
    sessions = {}
    for elt in problem.failures.only(*only):
        status = "Fail"
        sessions[elt.session.date.strftime("%d/%m/%Y")] = (elt.session.id, "f")
    for elt in problem.zones.only(*only):
        status = "Zone"
        sessions[elt.session.date.strftime("%d/%m/%Y")] = (elt.session.id, "z")
    for elt in problem.tops.only(*only):
        status = "Top"
        sessions[elt.session.date.strftime("%d/%m/%Y")] = (elt.session.id, "t")

    return render(request, 'gymstats/problem.html', {
        "problem": problem,
        "rating": avg_rating,
        "status": status,
        "ric": avg_ric,
        "sessions": sessions
    })


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
            'review_error_message': "Error while handling review - try again",
        })
    else:
        r = Review(reviewer=climber, comment=comment, problem=problem, rating=rating)
        r.save()
        return HttpResponseRedirect(reverse('gs:pb-review-display', args=(problem.id, r.id,)))


def problem_ric(request, problem_id, ric_id):
    problem = get_object_or_404(Problem, id=problem_id)
    try:
        ric = problem.ric_set.get(id=ric_id)
    except RIC.DoesNotExist:
        raise Http404("RIC does not exist")
    return render(request, 'gymstats/ric.html', {'ric': ric})


def evaluate_ric_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    try:
        risk = int(request.POST['risk'])
        intensity = int(request.POST['intensity'])
        complexity = int(request.POST['complexity'])
        climber = get_object_or_404(Climber, name="Thomas")  # TODO: retrieve logged in Climber
    except KeyError:
        return render(request, 'gymstats/problem.html', {
            'problem': problem,
            'ric_error_message': "Error while handling RIC - try again",
        })
    else:
        ric = RIC(reviewer=climber, problem=problem, risk=risk, intensity=intensity, complexity=complexity)
        ric.save()
        return HttpResponseRedirect(reverse('gs:pb-ric-display', args=(problem.id, ric.id,)))


def problem_searchbar(request):
    return render(request, 'gymstats/problem_searchbar.html')


def problem_search_results(request):
    try:
        # get comment from POST
        raw_filters = request.POST['search']
        parsed, unparsed = parse_filters(raw_filters)
        problems, stats = query_problems_from_filters(parsed)
    except KeyError:
        return render(request, 'gymstats/problem_results.html', {
            'results': [],
            'stats': {},            
            'filters': {},
            'unparsed': ["no filters provided"],            
            'error_message': "No filters provided",
        })
    except ParseError:
        return render(request, 'gymstats/problem_results.html', {
            'results': [],
            'stats': {},            
            'filters': {},
            'unparsed': [raw_filters],            
            'error_message': "Unable to parse given filters",
        })
    except SearchError:
        return render(request, 'gymstats/problem_results.html', {
            'results': [],
            'stats': {},            
            'filters': parsed,
            'unparsed': unparsed,            
            'error_message': "Search failed, try again later...",
        })
    else:
        return render(request, 'gymstats/problem_results.html', 
                    {
                        'results': problems,
                        'stats': stats,
                        'filters': parsed,
                        'unparsed': unparsed
                    })
