import datetime

from typing import List, Dict, Set, Any

import pandas as pd

from gymstats.models import Session, Gym, Top, Problem, Failure, Zone, HandHold, Footwork, ProblemMethod
from gymstats.helper.utils import float_duration_to_hour
from gymstats.helper.names import ATPS, TOP_ATPS, ZONE_ATPS, RANK, PREV
from gymstats.helper.names import RANK_TO_ID, Rank
from gymstats.statistics.pandas import df_achievements, df_attempts, df_by_rank, df_hard_tops, df_tops, df_by_wall_type, features_overrepr


def statistics(sessions: List[Session], start_date: datetime.date, 
               achievements: bool = True, hard_tops: bool = True,
               threshold_positions: Dict[Gym, List[int]] = None,
               compute_prev: bool = False) -> Dict[str, Any]:

    result = base_sessions_stats(sessions)
    
    # Create the DataFrame containing all relevant information
    df, _ = sessions_to_pandas(sessions, start_date, threshold_positions, compute_prev=compute_prev)

    if achievements:
        result = df_achievements(df, result)
    
    if hard_tops:
        result["hard_tops"] = df_hard_tops(df)

    return result


def summary(sessions: List[Session], threshold_positions: Dict[Gym, List[int]],
            start_date: datetime.date) -> Dict[str, Any]:
    """
    Compute various stats to store as IntervalStatistics for a Climber
    General:
    - General:
        - number of sessions, training hours, total boulders, total boulder attempts
        - total new boulder topped, total new hard boulders topped
    - Achievements
        - new Flash/Top/Zone/Fail: by difficulty
    - Wall types: 
        - overhanging/slab/vertical... : Fl/T/Z/F
        - same in expected and higher diff
    - Hand Holds / Foot Holds / Methods:
        - strength and weaknesses
    """
    results = {
        "General": {},
        "Achievements": {},
    }
    
    df, id_to_pb = sessions_to_pandas(sessions, start_date, threshold_positions, compute_prev=True)

    # General
    results["General"] = base_sessions_stats(sessions)
    results["General"]["boulders"] = len(df)
    results["General"]["attempts"] = df_attempts(df)
    results["General"]["new tops"] = df_tops(df)
    results["General"]["new hard tops"] = df_hard_tops(df)

    # Achievements
    for v in Rank:
        results["Achievements"][v.value] = df_by_rank(df, RANK_TO_ID[v])
    
    # Wall Type
    wall_types = _serie_wall_type_fast(df, id_to_pb) if id_to_pb else _serie_wall_type_slow(df)
    results["Wall Types"]  = df_by_wall_type(df, wall_types)

    # Hand Holds, Foot, Method, ...
    sw = {}
    results["Strengths & Weaknesses"] = sw
    # all
    sw["Overall"] = strength_and_weaknesses(df, id_to_pb)
    # hard
    sw["Hard"] = strength_and_weaknesses(df[df[RANK] > 0], id_to_pb)

    return results


def base_sessions_stats(sessions: List[Session]) -> Dict[str, Any]:
    duration = sum(s.duration for s in sessions)
    return {
        "sessions": len(sessions),
        "duration": duration,
        "duration_human_readable": float_duration_to_hour(duration)
    }


def strength_and_weaknesses(df: pd.DataFrame, id_to_pb: Dict[int, Problem], max_pvalue: float = 0.2) -> Dict[str, Any]:
    results = {}
    
    attrs = [
        ("Hand", _serie_handholds_fast),
        ("Foot", _serie_footworks_fast),
        ("Method", _serie_pb_methods_fast)
        ]

    # TODO: only new tops? only new tops and remove old tops?
    grp = df[TOP_ATPS] > 0
    
    for name, fn in attrs:
        features = fn(df, id_to_pb).str.get_dummies()
        out_df = features_overrepr(grp, features)
        results[name] = out_df[out_df["P-Value"]<= max_pvalue].to_dict()

    return results


def _serie_handholds_fast(df: pd.DataFrame, id_to_pb: Dict[int, Problem]) -> pd.Series:
    """
    Return a pandas Serie containing hand holds for each problem of the given DataFrame.
    Fastest method since it use cached Problems associated with the DataFrame.
    """
    return df.apply(lambda row: str(id_to_pb[row.name].str_repr(HandHold)), axis=1)


def _serie_footworks_fast(df: pd.DataFrame, id_to_pb: Dict[int, Problem]) -> pd.Series:
    """
    Return a pandas Serie containing footwork for each problem of the given DataFrame.
    Fastest method since it use cached Problems associated with the DataFrame.
    """
    return df.apply(lambda row: str(id_to_pb[row.name].str_repr(Footwork)), axis=1)


def _serie_pb_methods_fast(df: pd.DataFrame, id_to_pb: Dict[int, Problem]) -> pd.Series:
    """
    Return a pandas Serie containing problem methods for each problem of the given DataFrame.
    Fastest method since it use cached Problems associated with the DataFrame.
    """
    return df.apply(lambda row: str(id_to_pb[row.name].str_repr(ProblemMethod)), axis=1)


def _serie_wall_type_fast(df: pd.DataFrame, id_to_pb: Dict[int, Problem]) -> pd.Series:
    """
    Return a pandas Serie containing problem wall type for each problem of the given DataFrame.
    Fastest method since it use cached Problems associated with the DataFrame.
    """
    return df.apply(lambda row: str(id_to_pb[row.name].problem_type), axis=1)


def _serie_wall_type_slow(df: pd.DataFrame) -> pd.Series:
    """
    Return a pandas Serie containing problem wall type for each problem of the given DataFrame.
    """
    return df.apply(lambda row: str(Problem.objects.get(id=row.name).problem_type), axis=1)


def sessions_to_pandas(sessions: List[Session], start_date: datetime.date, 
                       threshold_positions: Dict[Gym, List[int]],
                       compute_prev: bool = True, pb_filter: Set[Problem] = None) -> pd.DataFrame:
    sessions = sorted(sessions, key = lambda s: s.date)
    summary = {}
    # TODO: decide whether or not we want to return id_to_pb
    # it accelerates the calculation of 'wall types' series (x50)
    id_to_pb = {}

    for session in sessions:
        for top in session.tops.all():
            if pb_filter and not top.problem in pb_filter:
                continue
            pid = top.problem.id
            atps = top.attempts 
            if pid not in summary:
                id_to_pb[pid] = top.problem
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
                id_to_pb[pid] = zone.problem
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
                id_to_pb[pid] = fail.problem
                r = RANK_TO_ID[fail.problem.rank(threshold_positions)]
                summary[pid] = [atps, -1, -1, r, -1]
                # same as above, do not compute previous achievement..
            else:
                summary[pid][0] += atps
                # all other cases need not be evaluated since its a failure
    
    # to pandas DataFrame
    df = pd.DataFrame(summary).transpose()
    df.columns = [ATPS, ZONE_ATPS, TOP_ATPS, RANK, PREV]
    return df, id_to_pb
