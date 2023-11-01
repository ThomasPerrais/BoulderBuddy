from typing import Dict, List
from functools import reduce
from gymstats.models import IndoorBoulder, Footwork, HandHold, ClimbingMove, Climber, Top
from gymstats.helper.names import *
from gymstats.statistics.base import fisher_overrepr
from gymstats.statistics.problems import attr_statistics
from django.db.models import Q, Prefetch



_attr_map = {
    HANDHOLD: HandHold,
    FOOTWORK: Footwork,
    MOVE: ClimbingMove
}


def query_problems_from_filters(parsed: Dict[str, Dict[str, List[str]]], climber: Climber):
    """
    query problems given list of parsed filters
    """
    problems = IndoorBoulder.objects.prefetch_related(Prefetch('tops', queryset=Top.objects.filter(session__climber=climber))).all()

    # TODO: test for statistics change this
    achievement = "all"
    for key, val in parsed.items():
        if key in {"top", "fail"}:
            achievement = key
            continue
        problems = _add_filter(problems, key, val)

    # filtering on achievement at the end so that we can extract stats
    fisher_stats = {}
    if achievement != "all" and climber:
        superset_stats = attr_statistics(problems)
        superset_size = len(problems)
        if achievement == "top":
            problems = problems.filter(~Q(tops=None))
        else:
            problems = problems.filter(Q(tops=None))
        subset_stats = attr_statistics(problems)
        subset_size = len(problems)

        fisher_stats = fisher_overrepr(superset_stats, subset_stats, superset_size, subset_size)

    return problems, fisher_stats


def _add_filter(problems, k, v):

    if k in {GRADE, TYPE, GYM}:
        qs = __build_or_query(v["eq"], k)
        return problems.filter(reduce(lambda x,y: x | y, qs))
    elif k in {MOVE, HANDHOLD, FOOTWORK}:  # TODO: is this efficient??
        attributes = __get_attr_objects(v["eq"], k)
        subset = reduce(lambda x,y: x|y, [attr.problem_set.all() for attr in attributes])
        return problems & subset
    elif k == "top":
        return problems.filter(~Q(tops=None))
    elif k == "fail":
        return problems.filter(Q(tops=None))
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