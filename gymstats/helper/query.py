from typing import Dict, List
from functools import reduce
from ..models import Problem, Footwork, HandHold, ProblemMethod
from gymstats.helper.names import *
from django.db.models import Q


_attr_map = {
    HANDHOLD: HandHold,
    FOOTWORK: Footwork,
    METHOD: ProblemMethod
} 

def query_problems_from_filters(parsed: Dict[str, Dict[str, List[str]]]):
    """
    query problems given list of parsed filters
    """
    problems = Problem.objects.all()

    for key, val in parsed.items():
        problems = _add_filter(problems, key, val)

    return problems


def _add_filter(problems, k, v):

    if k in {GRADE, TYPE, GYM}:
        qs = __build_or_query(v["eq"], k)
        return problems.filter(reduce(lambda x,y: x | y, qs))
    elif k in {METHOD, HANDHOLD, FOOTWORK}:  # TODO: is this efficient??
        attributes = __get_attr_objects(v["eq"], k)
        subset = reduce(lambda x,y: x|y, [attr.problem_set.all() for attr in attributes])
        return problems & subset
    elif k == DATE:
        return problems
    else:
        return problems


def __build_or_query(values: List[str], filter: str):
    if filter == GRADE:
        return [Q(grade = __to_first_case(elt)) for elt in values]
    elif filter == TYPE:
        return [Q(grade = elt) for elt in values]
    elif filter == GYM:
        return [Q(gym__abv = elt.upper()) for elt in values]
    else:
        # weird: TODO throw Error
        return None


def __get_attr_objects(values, filter):
    query = reduce(lambda x,y: x|y, [Q(name=elt) for elt in values])
    return _attr_map[filter].objects.filter(query)


def __to_first_case(s):
    return s[0].upper() + s[1:]