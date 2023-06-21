import math
import random


def rand_name(size: int = 5):
    return "".join([chr(random.randint(97, 122)) for _ in range(size)])


def float_duration_to_hour(duration):
    f = float(duration)
    s = math.floor(f)
    dec = math.floor((f - s) * 60)
    return "{}h{}".format(s, dec)
