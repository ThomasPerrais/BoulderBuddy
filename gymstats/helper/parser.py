import re
from gymstats.helper.names import *
from gymstats.helper.grade_order import GRADE_ORDER

filter_pattern = re.compile('(?P<key>.*) ?(?P<comparer>(eq|gte|lte|lt|gt|<|>|=|:)) ?(?P<values>.*)')

_map = {
    HANDHOLD: {"handholds","handhold","hh", "h"},
    FOOTWORK: {"footwork", "footworks", "fw", "f"},
    MOVE: {"moves", "move", "m"},
    TYPE: {"type", "problem-type", "t"},
    GRADE: {"grade", "g"},
    GYM: {"gym", "brand", "abv", "gym-abv"},
    DATE: {"date", "", "d"},
}

def parse_filters(raw_filters: str):
    """
    Parse raw filters written in the search bar
    """
    parsed = {}
    unparsed = []

    for elt in raw_filters.split(';'):
        match = filter_pattern.search(elt.replace("<=", " lte ").replace(">=", " gte "))
        if not match:
            if elt.strip() in {"removed", "rm"}:
                parsed["rm"] = True
                continue
            elif elt.strip() in {"!removed", "!rm"}:
                parsed["rm"] = False
                continue
            elif elt in {'top', 'fail'}:
                parsed[elt] = True
                continue
            else:
                unparsed.append("Pattern unknown: " + elt)
                continue

        # finding standardized key from "key"
        key = match.group("key").strip().lower()
        standardized_key = None
        for k, v in _map.items():
            if key in v:
                standardized_key = k
                break
        if not standardized_key:
            unparsed.append("Key unknown: " + elt)
            continue
        
        # standardized comparer
        comparer = match.group('comparer')
        if comparer in {"=", ":"}:
            comparer = "eq"
        elif comparer == "<":
            comparer = "lt"
        elif comparer == "<=":
            comparer = "lte"
        elif comparer == ">":
            comparer = "gt"
        elif comparer == ">=":
            comparer = "gte"
        
        # sanity check:
        if standardized_key in {"handhold", "footwork", "method", "type", "gym"}:
            if comparer != "eq":
                unparsed.append("Unadapted comparer: " + elt)
                continue

        # parsing values
        values = re.split("[ ,]", match.group("values").strip().lower())
        # sanity check
        if comparer != "eq" and len(values) > 1:
            unparsed.append("Too many values given comparer: " + elt)
            continue

        if standardized_key not in parsed:
            parsed[standardized_key] = {comparer: set(values)}
        elif comparer in parsed[standardized_key]:
            parsed[standardized_key][comparer].update(values)
        else:
            parsed[standardized_key][comparer] = set(values)
    
    # post-processing grades
    if GRADE in parsed and any(map(lambda x: x in parsed[GRADE], ["lt", "gt", "lte", "gte"])):
        if GYM in parsed:  # TODO: handle special case of gyms from same brand having different grade orders (Bloc Session...)
            vals = list({elt[:2] for elt in parsed[GYM]["eq"]})
            if len(vals) > 1:
                unparsed.append("several gym brand and comparer on grade can lead to inacurate results")
                order = GRADE_ORDER["@default"]
            else:
                try:
                    order = GRADE_ORDER[vals[0]]
                except KeyError:
                    unparsed.append("unknown grade order for gym")
                    order = GRADE_ORDER["@default"]
        else:
            unparsed.append("no gym and comparer on grade can lead to inacurate results")
            order = GRADE_ORDER["@default"]
        
        # now we have order and can fill "eq"
        res = set()
        for k, v in parsed[GRADE].items():
            if k == "eq":
                res.update(v)
            elif k.startswith("lt"):
                grade = list(v)[0]
                res.update(__grades_below(grade, order))
                if k == "lte":
                    res.add(grade)
            elif k.startswith("gt"):
                grade = list(v)[0]
                res.update(__grades_above(grade, order))
                if k == "gte":
                    res.add(grade)
            else:
                # weird
                unparsed.append("unknown comparer in grade")
        
        parsed[GRADE] = {"eq": res }

    if 'top' in parsed and 'fail' in parsed:
        del parsed["top"]
        del parsed["fail"]

    # turning sets to lists
    for key in parsed:
        if type(parsed[key]) == dict:
            for comparer in parsed[key]:
                parsed[key][comparer] = list(parsed[key][comparer])

    return parsed, unparsed


def __grades_below(grade, order):
    return __grades_above_or_below(grade, order, False)


def __grades_above(grade, order):
    return __grades_above_or_below(grade, order, True)


def __grades_above_or_below(grade, order, above):
    try:
        pos = order.index(grade)
        if above:
            return order[pos + 1:]
        else:
            return order[:pos]
    except ValueError:
        return []