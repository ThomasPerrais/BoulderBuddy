import builtins
import datetime
import math
import itertools
import pandas as pd

from typing import List, Dict, Hashable, Set
from collections import defaultdict

from gymstats.models import Try, Session, Gym, Rank, Top, Problem, Failure, Zone
from gymstats.helper.utils import float_duration_to_hour
from gymstats.statistics.tries import tops_stats


RANK_TO_ID = {
    Rank.UNK: -1,
    Rank.LOWER: 0,
    Rank.EXPECT: 1,
    Rank.HIGHER: 2,
}

ID_TO_RANK = {
    -1: Rank.UNK.value,
    0: Rank.LOWER.value,
    1: Rank.EXPECT.value,
    2: Rank.HIGHER.value,
}


def statistics(sessions: List[Session], start_date: datetime.date, 
               achievements: bool = True, hard_tops: bool = True,
               threshold_positions: Dict[Gym, List[int]] = None,
               compute_prev: bool = False):

    result = base_sessions_stats(sessions)
    
    # Create the DataFrame containing all relevant information
    df = sessions_to_pandas(sessions, start_date, threshold_positions, compute_prev=compute_prev)

    if achievements:
        result = df_achievements(df, result)
    
    if hard_tops:
        result["hard_tops"] = df_hard_tops(df)

    return result


def base_sessions_stats(sessions: List[Session]):
    duration = sum(s.duration for s in sessions)
    return {
        "sessions": len(sessions),
        "duration": duration,
        "duration_human_readable": float_duration_to_hour(duration)
    }


def df_achievements(df: pd.DataFrame, res: Dict = None):
    """
    Compute the number of flash, top, zone, fail and try of the given summary DataFrame.
    Statistics are computed per difficulty when the information is available (Lower, Expect, Higher)
    """
    result = {} if not res else res
    achievements = ["try", "fail", "zone", "top", "flash"]
    for v in Rank:
        for a in achievements:
            result["pb_{}_{}".format(v.value, a)] = 0

    for key, grp in df.groupby("rank"):
        prefix = "pb_" + ID_TO_RANK[key] + "_"
        result[prefix + "try"] = len(grp)

        for topped, subgrp in grp.groupby(grp["top attempts"] != -1):
            if topped:
                # Flashes must have top attempts = 1 and should not have been tried before (previous = -1)
                result[prefix + "flash"] = sum(subgrp[subgrp["previous"] == -1]["top attempts"] == 1)
                result[prefix + "top"] = len(subgrp) - result[prefix + "flash"]
            else:
                result[prefix + "fail"] = sum(subgrp["zone attempts"] == -1)
                result[prefix + "zone"] = len(subgrp) - result[prefix + "fail"]

    for a in achievements:
        result["pb_all_" + a] = sum(result["pb_{}_{}".format(v.value, a)] for v in Rank)
    
    return result


def df_hard_tops(df: pd.DataFrame):
    """
    Compute the number of *new* hard tops given the summary DataFrame of a list of sessions.
    A *new* top is a top ('top attempts' > 0) on a boulder that wasn't topped before ('previous' < 2)
    A *hard* top is a top on a hard boulder ('rank' > 0) given User thresholds.
    """
    return len(df[(df["rank"] > 0) & (df["top attempts"] > 0) & (df["previous"] < 2)])


def sessions_to_pandas(sessions: List[Session], start_date: datetime.date, 
                       threshold_positions: Dict[Gym, List[int]],
                       compute_prev: bool = True, pb_filter: Set[Problem] = None):
    sessions = sorted(sessions, key = lambda s: s.date)
    summary = {}

    for session in sessions:
        for top in session.tops.all():
            if pb_filter and not top.problem in pb_filter:
                continue
            pid = top.problem.id
            atps = top.attempts 
            if pid not in summary:
                r = RANK_TO_ID[top.problem.rank(threshold_positions)]
                summary[pid] = [atps, atps, atps, r, -1]
                if compute_prev:
                    if Top.objects.filter(problem=top.problem, session__date__lt=start_date).count() > 0:
                        summary[pid][-1] = 2
                    elif Zone.objects.filter(problem=top.problem, session__date__lt=start_date).count() > 0:
                        summary[pid][-1] = 1
                    elif Failure.objects.filter(problem=top.problem, session__date__lt=start_date).count() > 0:
                        summary[pid][-1] = 0
            else:
                summary[pid][0] += top.attempts
                if summary[pid][1] == -1:
                    # problem wasn't zoned before -> set zone and top to current attempts
                    summary[pid][1] = summary[pid][0]
                    summary[pid][2] = summary[pid][0]
                elif summary[pid][2] == -1:
                    # problem wasn't topped before -> set top to current attempts, left zone unchanged
                    summary[pid][2] = summary[pid][0]
                # last case: problem was already topped, we do nothing except adding to attempts 

        for zone in session.zones.all():
            if pb_filter and not zone.problem in pb_filter:
                continue
            pid = zone.problem.id
            atps = zone.attempts
            if pid not in summary:
                r = RANK_TO_ID[zone.problem.rank(threshold_positions)]
                summary[pid] = [atps, atps, -1, r, -1]
                # here we do not compute prev. This means we don't care about side effects regarding zones..
                # Need to change this behaviour if we want exact stats on new zones
            else:
                summary[pid][0] += atps
                if summary[pid][1] == -1:
                    # problem wasn't zoned before -> set zone to current attempts
                    summary[pid][1] = summary[pid][0]
        
        for fail in session.failures.all():
            if pb_filter and not fail.problem in pb_filter:
                continue
            pid = fail.problem.id
            atps = fail.attempts
            if pid not in summary:
                r = RANK_TO_ID[fail.problem.rank(threshold_positions)]
                summary[pid] = [atps, -1, -1, r, -1]
                # same as above, do not compute previous achievement..
            else:
                summary[pid][0] += atps
                # all other cases need not be evaluated since its a failure
    
    # to pandas DataFrame
    df = pd.DataFrame(summary).transpose()
    df.columns = ["attempts", "zone attempts", "top attempts", "rank", "previous"]
    return df


# @deprecated("Use sessions_to_pandas instead")
def get_problem_achievement(sessions, pb_filter: Set[Problem] = None) -> Dict[Problem, str]:
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


# @deprectaed("use sessions_to_pandas instead")
def sessions_tops_stats(sessions: List[Session], start_date: datetime.date, 
                        threshold_positions: Dict[Gym, List[int]], all: bool = True,
                        lower: bool = True, expect: bool = True, higher: bool = True,
                        unk: bool = True):
    """
    Compute *tops* statistical summary on the given list of sessions. Summary include:
    - total number of tops
    - total number of attempts
    - total number of problems
    - total number of *new* tops
    If User threshold is given, also compute statistical summary for the different classes of *problems* (lower, expect, higher, unk) 
    """
    
    # used to store all tops infos
    results = {}  

    all_tops = list(itertools.chain(*[s.tops.all() for s in sessions]))
    
    # TODO: add condition to use it or not
    new_tops = set()  # if *all = True*: will be populated with new tops so that we won't have to check again in subsequent calls
    new_flashes = set()

    if all:
        results["all"] = tops_stats(all_tops, start_date, new_tops, new_flashes)
    
    if threshold_positions:
        # necessary to compute stats on Lower, Expect and Higher problems

        if lower:
            low_tops = [t for t in all_tops if t.problem.rank(threshold_positions) == Rank.LOWER]
            results["lower"] = tops_stats(low_tops, start_date, new_tops, new_flashes)
        
        if expect:
            expect_tops = [t for t in all_tops if t.problem.rank(threshold_positions) == Rank.EXPECT]
            results["expect"] = tops_stats(expect_tops, start_date, new_tops, new_flashes)

        if higher:
            higher_tops = [t for t in all_tops if t.problem.rank(threshold_positions) == Rank.HIGHER]
            results["higher"] = tops_stats(higher_tops, start_date, new_tops, new_flashes)
        
        if unk:
            unk_tops = [t for t in all_tops if t.problem.rank(threshold_positions) == Rank.UNK]
            results["unk"] = tops_stats(unk_tops, start_date, new_tops, new_flashes)
    

    results["new-tops-list"] = new_tops
    results["new-flashes-list"] = new_flashes
    return results
