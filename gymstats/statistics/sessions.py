import builtins
import datetime
import math
import itertools

from typing import List, Dict, Hashable
from collections import defaultdict

from gymstats.models import Try, Session, Gym, Rank, Top, Problem
from gymstats.helper.utils import float_duration_to_hour
from gymstats.helper.grade_order import GRADE_ORDER, BRAND_TO_ABV


def statistics(sessions: List[Session], start_date: datetime.date, duration: bool = True, length: bool = True, 
               top_zone_fail: bool = True, hard_tops: bool = True, threshold_positions: Dict[Gym, List[int]] = None):

    result = {}
        
    if length:
        result["sessions"] = len(sessions)
    
    if duration:
        result["duration"] = sum([s.duration for s in sessions])
        result["duration_human_readable"] = float_duration_to_hour(result["duration"])
    
    if top_zone_fail:
        problems_achievement = get_problem_achievement(sessions)

        # TODO: there might be a problem with flash (and other) if a problem was tried the previous month/year/...

        result["pb_all_try"] = 0
        result["pb_all_flash"] = 0
        result["pb_all_top"] = 0
        result["pb_all_zone"] = 0
        result["pb_all_fail"] = 0
        if threshold_positions:
            for v in Rank:
                result["pb_{}_try".format(v.value)] = 0
                result["pb_{}_flash".format(v.value)] = 0
                result["pb_{}_top".format(v.value)] = 0
                result["pb_{}_zone".format(v.value)] = 0
                result["pb_{}_fail".format(v.value)] = 0

        for problem, value in problems_achievement.items():
            r = problem.rank(threshold_positions)
            keys = ["pb_all_try", "pb_all_" + value, "pb_{}_try".format(r.value), "pb_{}_{}".format(r.value, value)]
            for k in keys:
                result[k] += 1
    
    if hard_tops:
        if not threshold_positions:
            # impossible to compute hard tops without climber threshold
            result["hard_tops"] = "NA"
        else:
            allowed = {Rank.EXPECT, Rank.HIGHER}  # problem ranked at least EXPECT 
            all_tops = itertools.chain(*[s.tops.all() for s in sessions])  # all tops in the current sessions set

            problems = { t.problem for t in all_tops if t.problem.rank(threshold_positions) in allowed }
            # need to check if some problems where topped the month before.
            result["hard_tops"] = 0
            for pb in problems:
                if Top.objects.filter(problem=pb, session__date__lt=start_date).count() == 0:
                    # problem was topped before the given start date of the session set
                    # this means that it is not an actual new top of the given time slot
                    result["hard_tops"] += 1

    return result


def get_problem_achievement(sessions, pb_filter: builtins.set[Problem] = None) -> Dict[Problem, str]:
    problems_achievement = {}
    for sess in sessions:
        for top in sess.tops.all():
            if pb_filter and not top.problem in pb_filter:
                continue
            if top.problem not in problems_achievement:
                # problem not known -> either flashed ot topped
                problems_achievement[top.problem] = "flash" if top.attempts == 1 else "top"
            else:
                # problem was already tried
                # if it was flashed do not change anything
                # otherwise it is now topped.
                if problems_achievement[top.problem] != "flash":
                    problems_achievement[top.problem] = "top"
        
        for zone in sess.zones.all():
            if pb_filter and not zone.problem in pb_filter:
                continue
            if zone.problem not in problems_achievement:
                # problem not known -> zone
                problems_achievement[zone.problem] = "zone"
            else:
                # problem was already tried
                # only change if it was failed
                if problems_achievement[zone.problem] == "fail":
                    problems_achievement[zone.problem] = "zone"
        
        for fail in sess.failures.all():
            if pb_filter and not fail.problem in pb_filter:
                continue
            if fail.problem not in problems_achievement:
                # problem not known -> fail
                # no else since it cannot be worse
                problems_achievement[fail.problem] = "fail"
    
    return problems_achievement