GRADE_ORDER = {
    "@default": ["white", "yellow", "orange", "green", "blue", "red", "black", "purple"],
    "cd": ["yellow", "orange", "green", "blue", "pink", "red", "black", "purple"],
    "va": ["white", "orange", "green", "blue", "red", "black", "purple"],
    "bo": ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13", "b14"],
    "bs": ["blue", "green", "orange", "pink", "black", "gray", "white"],
    "bl": ["yellow", "orange", "blue", "red", "green", "black"],
    # special cases
    "bsm": ["blue", "green", "red", "pink", "black", "gray"],
}

BRAND_TO_ABV = {
    "Boulder Line": "bl",
    "Climbing District": "cd",
    "Vertical'Art": "va",
    "Block'Out": "bo",
    "Bloc Session": "bs",
}


def grades_list(gym, default=True):
    values = []
    # check for special cases
    if gym.abv.lower() in GRADE_ORDER:
        values = GRADE_ORDER[gym.abv.lower()]
    elif gym.brand in BRAND_TO_ABV:
        values = GRADE_ORDER[BRAND_TO_ABV[gym.brand]]
    elif default:
        values = GRADE_ORDER["@default"]
    return [elt[0].upper() + elt[1:] for elt in values]
