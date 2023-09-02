from gymstats.models import Gym, Problem, Top, Zone, Failure, Session, Climber
from gymstats.helper.grade_order import grades_list
from gymstats.statistics.sessions import get_problem_achievement


achievements = ["flash", "top", "zone", "fail", "not tried"]


def current_problems_achievement(gym: Gym, cl: Climber, handle_unk="keep"):

    result = {}
    result["labels"] = grades_list(gym, default=True)
    grade_map = {elt: i for i, elt in enumerate(result["labels"])}

    for achievement in achievements:
        result[achievement] = [0] * len(grade_map)

    # problems currently in gym
    problems = set(gym.problem_set.filter(removed=False))

    if len(problems) == 0:
        return result

    earliest_date = min([pb.date_added for pb in problems])

    sessions = Session.objects.filter(climber=cl, date__gte=earliest_date, gym=gym).order_by("date")

    problems_achievement = get_problem_achievement(sessions, pb_filter=problems)

    for pb in problems:
        grade = pb.grade
        if grade not in grade_map and handle_unk == "group":
            grade = "unknown"
        
        if grade not in grade_map:
            if handle_unk in {"keep", "group"}:
                # Keeping unknown grades
                grade_map[grade] = len(grade_map)
                for achievement in achievements:
                    result[achievement].append(0)
                result["labels"].append(grade)
            else:
                # problem is not taken into account since its grade is unknown in the grade scale...
                continue
        
        # at this point *grade* is necessarily in grade_map
        result[problems_achievement.get(pb, "not tried")][grade_map[grade]] += 1

    return result
