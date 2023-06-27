GRADE_ORDER = {
    "@default": ["white", "yellow", "orange", "green", "blue", "red", "black", "purple"],
    "cd": ["yellow", "orange", "green", "blue", "pink", "red", "black", "purple"],
    "va": ["white", "orange", "green", "blue", "red", "black", "purple"],
    "bo": ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13", "b14"],
    "bs": ["blue", "green", "orange", "pink", "black", "gray", "white"],
}

BRAND_TO_ABV = {
    "Climbing District": "cd",
    "Vertical'Art": "va",
    "Block'Out": "bo",
    "Bloc Session": "bs",
}


def grades_list(gym, default=True):
    values = []
    if gym.brand in BRAND_TO_ABV:
        values = GRADE_ORDER[BRAND_TO_ABV[gym.brand]]
    elif default:
        values = GRADE_ORDER[BRAND_TO_ABV["@default"]]
    return [elt[0].upper() + elt[1:] for elt in values]
