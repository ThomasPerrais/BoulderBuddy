from collections import defaultdict
from scipy.stats import fisher_exact
from typing import List, Dict

from gymstats.models import Problem, Footwork, HandHold, ProblemMethod, ProblemType
from gymstats.helper.names import TYPE_ABV, METHOD_ABV, FOOTWORK_ABV, HANDHOLD_ABV


def attr_statistics(pbs: List[Problem]):
    stats = {
        TYPE_ABV: defaultdict(int),
        HANDHOLD_ABV: defaultdict(int),
        FOOTWORK_ABV: defaultdict(int),
        METHOD_ABV: defaultdict(int)
    }
    for pb in pbs:
        stats[TYPE_ABV][str(pb.problem_type)] += 1
        for h in pb.hand_holds.all():
            stats[HANDHOLD_ABV][str(h)] += 1
        for f in pb.footwork.all():
            stats[FOOTWORK_ABV][str(f)] += 1
        for m in pb.problem_method.all():
            stats[METHOD_ABV][str(m)] += 1
    return stats


def fisher_overrepr(superset_stats: Dict, subset_stats: Dict, superset_size: int,
                    subset_size: int, maxpvalue: float = 0.4, topk: int = 3):
    res = {}
    for attr in superset_stats: 
        current = []
        for val in superset_stats[attr]:
            superset_occ = superset_stats[attr][val]
            subset_occ = subset_stats[attr][val]  # should always work if we use defaultdict

            fisher_stat = fisher_exact([[subset_occ, superset_occ], [subset_size - subset_occ, superset_size - superset_occ]])
            if fisher_stat.pvalue < maxpvalue and fisher_stat.statistic != float("+inf") and fisher_stat.statistic > 1:
                current.append((val, fisher_stat.statistic, fisher_stat.pvalue))
        res[attr] = sorted(current, key=lambda t: t[1], reverse=True)[:topk]
    return res