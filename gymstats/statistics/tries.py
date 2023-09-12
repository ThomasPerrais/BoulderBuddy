import datetime

from typing import List, Set
from deprecated import deprecated

from gymstats.models import Try, Top, Problem, Zone, Failure


@deprecated(reason="method should not be used anymore")
def tops_stats(tops: List[Top], start_date: datetime.date, 
               new_tops: Set[Top] = None, new_flashes: Set[Top] = None):
    """
    Extract statistics from a list of tops
    """

    problems = { t.problem for t in tops }
    
    results = __base_stats(tops, problems)

    # II - new achievements
    results["new"] = 0
    results["new-flash"] = 0
    for pb in problems:
        nt = False
        if new_tops and pb in new_tops:
            nt = True
        elif Top.objects.filter(problem=pb, session__date__lt=start_date).count() == 0:
            nt = True
            if new_tops: 
                new_tops.add(pb)

        if nt:
            results["new"] += 1

            if new_flashes and pb in new_flashes:
                results["new_flash"] += 1
            else:
                first_time_flash = sorted([t for t in tops if t.problem == pb], key=lambda t: t.session.date)[0].attempts == 1
                zoned = Zone.objects.filter(problem=pb, session__date__lt=start_date).count()
                failed = Failure.objects.filter(problem=pb, session__date__lt=start_date).count() 

                if first_time_flash and (not zoned) and (not failed):
                    results["new-flash"] += 1
                    if new_flashes:
                        new_flashes.add(pb)
            
    return results


def __base_stats(tries: List[Try], problems: Set[Problem]):
    return {
        "length": len(tries),
        "volume": sum(t.attempts for t in tries),
        "problems": len(problems),
    }
