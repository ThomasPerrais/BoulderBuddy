from collections import defaultdict
from typing import List

from gymstats.models import Problem
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