from gymstats.models import Gym, Problem, Top, Zone, Failure, Session, Climber
from gymstats.helper.grade_order import grades_list
from gymstats.statistics.sessions import get_problem_achievement, sessions_to_pandas


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

    earliest_date = min(pb.date_added for pb in problems)

    sessions = Session.objects.filter(climber=cl, date__gte=earliest_date, gym=gym).order_by("date")

    # no need to specify start_date and no need to compute prev since none of the assessed problems
    # were present before the earliest_date by definition.
    df = sessions_to_pandas(sessions, None, None, False, pb_filter=problems)

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
        achievement = "not tried"
        if pb.id in df.index:
            row = df.loc[pb.id]
            if row["top attempts"] == 1:
                achievement = "flash"
            elif row["top attempts"] > 0:
                achievement = "top"
            elif row["zone attempts"] > 0:
                achievement = "zone"
            else:
                achievement = "fail"
        result[achievement][grade_map[grade]] += 1

    return result
