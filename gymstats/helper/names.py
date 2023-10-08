from enum import Enum


HANDHOLD = "handhold"
FOOTWORK = "footwork"
TYPE = "type"
MOVE = "move"
GRADE = "grade"
GYM = "gym"
DATE = "date"


TYPE_ABV = "ty"
HANDHOLD_ABV = "hh"
FOOTWORK_ABV = "fw"
METHOD_ABV = "me"


ATPS = "attempts"
TOP_ATPS = "top attempts"
ZONE_ATPS = "zone attempts"
RANK = "rank"
PREV = "previous"


class Achievement(Enum):
    FAIL = "fail"
    ZONE = "zone"
    TOP = "top"
    FLASH = "flash"


# TODO: maybe give int values to Rank instead of string values?
class Rank(Enum):
    UNK = "unk"
    LOWER = "lower"
    EXPECT = "expect"
    HIGHER = "higher"


RANK_TO_ID = {
    Rank.UNK: -1,
    Rank.LOWER: 0,
    Rank.EXPECT: 1,
    Rank.HIGHER: 2,
}

ID_TO_RANK = {
    -1: Rank.UNK.value,
    0: Rank.LOWER.value,
    1: Rank.EXPECT.value,
    2: Rank.HIGHER.value,
}
