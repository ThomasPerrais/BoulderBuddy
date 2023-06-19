import math

from typing import List, Dict
from collections import defaultdict

from gymstats.models import Try, Session, Gym
from gymstats.helper.utils import float_duration_to_hour
from gymstats.helper.grade_order import GRADE_ORDER, BRAND_TO_ABV


def statistics(sessions: List[Session], duration: bool = True, length: bool = True, 
               top_zone_fail: bool = True, threshold: Dict[Gym, str] = None):

    result = {}

    if length:
        result["Sessions"] = len(sessions)
    
    if duration:
        result["duration"] = sum([s.duration for s in sessions])
        result["Training Hours"] = float_duration_to_hour(result["duration"])
    
    if top_zone_fail:
        problems_achievement = {}
        for sess in sessions:
            for top in sess.tops.all():
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
                if zone.problem not in problems_achievement:
                    # problem not known -> zone
                    problems_achievement[zone.problem] = "zone"
                else:
                    # problem was already tried
                    # only change if it was failed
                    if problems_achievement[zone.problem] == "fail":
                        problems_achievement[zone.problem] = "zone"
            
            for fail in sess.failures.all():
                if fail.problem not in problems_achievement:
                    # problem not known -> fail
                    # no else since it cannot be worse
                    problems_achievement[fail.problem] = "fail"
        
        # TODO: there might be a problem with flash (and other) if a problem was tried the previous month...

        result["pb_all_try"] = 0
        result["pb_all_flash"] = 0
        result["pb_all_top"] = 0
        result["pb_all_zone"] = 0
        result["pb_all_fail"] = 0
        if threshold:
            result["pb_lower_try"] = 0
            result["pb_lower_flash"] = 0
            result["pb_lower_top"] = 0
            result["pb_lower_zone"] = 0
            result["pb_lower_fail"] = 0

            result["pb_expect_try"] = 0
            result["pb_expect_flash"] = 0
            result["pb_expect_top"] = 0
            result["pb_expect_zone"] = 0
            result["pb_expect_fail"] = 0

            result["pb_higher_try"] = 0
            result["pb_higher_flash"] = 0
            result["pb_higher_top"] = 0
            result["pb_higher_zone"] = 0
            result["pb_higher_fail"] = 0

            result["pb_unk_try"] = 0
            result["pb_unk_flash"] = 0
            result["pb_unk_top"] = 0
            result["pb_unk_zone"] = 0
            result["pb_unk_fail"] = 0

        for problem, value in problems_achievement.items():
            keys = ["pb_all_try", "pb_all_" + value]
            if threshold:
                if problem.gym in threshold:
                    # scale order in the current gym
                    order = GRADE_ORDER[BRAND_TO_ABV[problem.gym.brand]]
                    try:
                        grade_pos = order.index(problem.grade.lower()) # position of problem grade in the scale
                        
                        threshold_positions = []
                        for grade in threshold[problem.gym].split(','):
                            low_gr = grade.lower()
                            if low_gr in order:
                                threshold_positions.append(order.index(low_gr))
                        threshold_positions = sorted(threshold_positions)

                        if len(threshold_positions) == 0:
                            # problem in threshold of the current user, need to update them
                            keys.append("pb_unk_try")
                            keys.append("pb_unk_" + value)
                        elif grade_pos < threshold_positions[0]:
                            keys.append("pb_lower_try")
                            keys.append("pb_lower_" + value)
                        elif grade_pos > threshold_positions[-1]:
                            keys.append("pb_higher_try")
                            keys.append("pb_higher_" + value)
                        else:
                            keys.append("pb_expect_try")
                            keys.append("pb_expect_" + value)

                    except KeyError:
                        # key error somewhere, maybe problem grade has an error
                        # default to 'unk'
                        keys.append("pb_unk_try")
                        keys.append("pb_unk_" + value)
                else:
                    # climber did not provide a threshold for this gym... adding to 'unk'
                    keys.append("pb_unk_try")
                    keys.append("pb_unk_" + value)
            
            for k in keys:
                result[k] += 1
    
    return result