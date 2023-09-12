from scipy.stats import fisher_exact
from typing import Dict, List


def fisher_overrepr(superset_stats: Dict, subset_stats: Dict, superset_size: int,
                    subset_size: int, maxpvalue: float = 0.4, topk: int = 3) -> Dict[str, List[(str, float, float)]]:
    results = {}
    for attr in superset_stats: 
        current = []
        for val in superset_stats[attr]:
            superset_occ = superset_stats[attr][val]
            subset_occ = subset_stats[attr][val]  # should always work if we use defaultdict

            fisher_stat = fisher_exact([[subset_occ, superset_occ], [subset_size - subset_occ, superset_size - superset_occ]])
            if fisher_stat.pvalue < maxpvalue and fisher_stat.statistic != float("+inf") and fisher_stat.statistic > 1:
                current.append((val, fisher_stat.statistic, fisher_stat.pvalue))
        results[attr] = sorted(current, key=lambda t: t[1], reverse=True)[:topk]
    return results

