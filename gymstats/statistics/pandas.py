from typing import Dict, Any

import pandas as pd

from gymstats.helper.names import ATPS, TOP_ATPS, ZONE_ATPS, RANK, PREV
from gymstats.helper.names import Achievement, ID_TO_RANK, Rank


def df_achievements(df: pd.DataFrame, res: Dict = None) -> pd.DataFrame:
    """
    Compute the number of flash, top, zone, fail and try of the given summary DataFrame.
    Statistics are computed per difficulty when the information is available (Lower, Expect, Higher)
    """
    results = {} if not res else res
    for v in Rank:
        for a in Achievement:
            results["pb_{}_{}".format(v.value, a.value)] = 0

    for key, grp in df.groupby("rank"):
        prefix = "pb_" + ID_TO_RANK[key] + "_"

        for topped, subgrp in grp.groupby(grp[TOP_ATPS] != -1):
            if topped:
                # Flashes must have top attempts = 1 and should not have been tried before (previous = -1)
                results[prefix + Achievement.FLASH.value] = sum(subgrp[subgrp[PREV] == -1][TOP_ATPS] == 1)
                results[prefix + Achievement.TOP.value] = len(subgrp) - results[prefix + Achievement.FLASH.value]
            else:
                results[prefix + Achievement.FAIL.value] = sum(subgrp[ZONE_ATPS] == -1)
                results[prefix + Achievement.ZONE.value] = len(subgrp) - results[prefix + Achievement.FAIL.value]

    for a in Achievement:
        results["pb_all_" + a.value] = sum(results["pb_{}_{}".format(v.value, a.value)] for v in Rank)
    
    return results


def df_by_rank(df: pd.DataFrame, rank: int) -> Dict[str, int]:
    """
    Compute achievements and stats by problem ranking.
    """
    rank_df = df[df[RANK] == rank]
    
    results = {
        "boulders": len(rank_df),
        "attempts": df_attempts(rank_df),
        "new flashes": df_flashes(rank_df),
        "new zones": df_zones(rank_df),
        "new fail": df_fails(rank_df)
    }

    results["new tops"] = df_tops(rank_df) - results["new flashes"]
    return results


def df_attempts(df: pd.DataFrame) -> int:
    """
    Compute the number of attempts of the given summary DataFrame
    """
    return sum(df[ATPS])


def df_hard_tops(df: pd.DataFrame) -> int:
    """
    Compute the number of *new* hard tops given the summary DataFrame of a list of sessions.
    A *new* top is a top ('top attempts' > 0) on a boulder that wasn't topped before ('previous' < 2)
    A *hard* top is a top on a hard boulder ('rank' > 0) given User thresholds.
    """
    return len(df[(df[RANK] > 0) & (df[TOP_ATPS] > 0) & (df[PREV] < 2)])


def df_flashes(df: pd.DataFrame) -> int:
    """
    Compute the number of *new* flashes given the summary DataFrame of a list of sessions.
    A *new* top is a flash ('top attempts' == 1) on a boulder that wasn't tried before ('previous' == -1)
    """
    return len(df[(df[TOP_ATPS] == 1) & (df[PREV] == -1)])


def df_tops(df: pd.DataFrame) -> int:
    """
    Compute the number of *new* tops given the summary DataFrame of a list of sessions.
    A *new* top is a top ('top attempts' > 0) on a boulder that wasn't topped before ('previous' < 2)
    """
    return len(df[(df[TOP_ATPS] > 0) & (df[PREV] < 2)])


def df_tops_all(df: pd.DataFrame) -> int:
    """
    Compute the total number tops given the summary DataFrame of a list of sessions ('top attempts' > 0).
    """
    return len(df[df[TOP_ATPS] > 0])


def df_zones(df: pd.DataFrame) -> int:
    """
    Compute the number of *new* zones given the summary DataFrame of a list of sessions.
    A *new* zone is a zone ('top attempts' == -1 & 'zone attempts' > 0) 
    on a boulder that wasn't zoned or topped before ('previous' < 1)
    """
    return len(df[(df[TOP_ATPS] == -1) & (df[ZONE_ATPS] > 0) & (df[PREV] < 1)])


def df_fails(df: pd.DataFrame) -> int:
    """
    Compute the number of *new* fails given the summary DataFrame of a list of sessions.
    A *new* fail is a fail ('zone attempts' == -1) 
    on a boulder that wasn't tried before ('previous' == -1)
    """
    return len(df[(df[ZONE_ATPS] == -1) & (df[PREV] == -1)])


def df_by_wall_type(df: pd.DataFrame, wall_types: pd.Series) -> Dict[str, Any]:
    """
    Compute wall types statistics
    """
    results = {}
    for t, grp in df.groupby(wall_types):
        results[t] = {
            "boulders": len(grp)
        }
        for r, subgrp in grp.groupby(RANK):
            new_tops = df_tops(subgrp)
            results[t][ID_TO_RANK[r]] = [new_tops, df_tops_all(df) - new_tops, len(subgrp)]

    return results
