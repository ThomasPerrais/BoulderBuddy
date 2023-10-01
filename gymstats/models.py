import datetime
import itertools
import os
import math

from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from enum import Enum
from location_field.models.plain import PlainLocationField
from picklefield.fields import PickledObjectField
from typing import Any,  Dict, List, Union

from gymstats.helper.utils import rand_name
from gymstats.helper.grade_order import grades_list
from gymstats.helper.names import Rank


### CLIMBING PLACES ###

class ClimbingPlace(models.Model):
    """
    Base class representing a place where one can do outdoor/indoor bouldering/rock climbing/lead/...
    """
    location = PlainLocationField(zoom=12)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        abstract = True


class Crag(ClimbingPlace):
    """
    Outdoor climbing place.
    """
    nearest_city=models.CharField(max_length=100)


class Gym(ClimbingPlace):
    """
    Indoor climbing place for bouldering or lead.
    """
    city = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    abv = models.CharField(max_length=10)

    # location = PlainLocationField(based_fields=['city'], zoom=12)

    class GymType(models.TextChoices):
        BOULDER = 'Boulder'
        LEAD = 'Lead'

    gym_type = models.CharField(max_length=10, choices=GymType.choices, default=GymType.BOULDER)

    def __str__(self) -> str:
        return "{} {} ({})".format(self.brand, self.city, self.gym_type)


### CLIMBING SHOES ###

class Shoes(models.Model):

    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    size = models.FloatField()
    purchase_date = models.DateField()

    def __str__(self) -> str:
        return self.brand + " " + self.name


class ShoesFixing(models.Model):

    fixing_date = models.DateField()
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE)  # CASCADE: when a shoe is deleted, delete shoe fixing entry

    def __str__(self) -> str:
        return "{}: {}".format(self.fixing_date, self.shoes)



### USERS & STATS ###

class Climber(models.Model):

    def upload_picture(instance, filename):
        _, ext = os.path.splitext(filename)
        return os.path.join('climbers', instance.name + "_" + rand_name() + ext)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=upload_picture, blank=True)

    class StatsPreference(models.IntegerChoices):
        WEEK = 1
        MONTH = 2
        YEAR = 3
        ALL_TIME = 4
    
    stats_preference = models.IntegerField(choices=StatsPreference.choices, default=1)

    month_hour_target = models.IntegerField(default=10)  # training hour target
    month_hard_boulder_target = models.IntegerField(default=10)  # target number of hard boulders to top every month

    preferred_gyms = models.ManyToManyField(Gym, blank=True, verbose_name="My Gyms")

    def thresholds(self) -> Dict[Gym, List[int]]:
        thresholds = {}
        for th in self.hard_boulders.all():
            order = grades_list(th.gym, default=True)
            positions = [order.index(g) for g in th.grade_threshold.split(',') if g in order]
            thresholds[th.gym] = sorted(positions)
        return thresholds

    def __str__(self) -> str:
        return self.name


class IntervalStatistics(models.Model):
    climber = models.ForeignKey(Climber, on_delete=models.CASCADE, related_name="past_statistics")

    interval_id = models.IntegerField() # id of the month (1..12) or week (1..52)
    year = models.IntegerField()

    class Intervals(models.IntegerChoices):
        WEEK = 1
        MONTH = 2
        YEAR = 3

    interval = models.IntegerField(choices=Intervals.choices)
    args = PickledObjectField()  # various statistics: hard boulder threshold, training time, hard boulders, ...


class HardBoulderThreshold(models.Model):
    climber = models.ForeignKey(Climber, on_delete=models.CASCADE, related_name="hard_boulders")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    grade_threshold = models.CharField(max_length=20)



### HOLDS & METHODS ###

class Describable(models.Model):

    def location(self, name):
        return os.path.join(self.location, name)

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to=location, blank=True)

    def __init__(self, location, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.location = os.path.join("problems", location)

    def __str__(self) -> str:
        return self.name


class HandHold(Describable): # choices: [jugs, slopers, pockets, pinches, crimps, edges, gaston, undercling, crack, volume]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('hand-holds', *args, **kwargs)


class Footwork(Describable):  # choices: [tiny, edging, smearing, heelhook, contre-pointe]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('footwork', *args, **kwargs)


class ProblemType(Describable):  # choices: [vertical, slab, overhanging, roof, traverse]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('problem-type', *args, **kwargs)


class ProblemMethod(Describable):  # choices: [dyno, coordo, lolotte, flex, mantle, ...]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('problem-method', *args, **kwargs)


### SECTORS ###

class Sector(models.Model):

    wall_types = models.ManyToManyField(ProblemType, blank=False)
    map = models.ImageField(upload_to='sectors-maps', blank=True)
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True   


class IndoorSector(Sector):

    sector_id = models.IntegerField()
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)  # deleting a gym -> delete its sectors
    
    def pretty_name(self):
        if len(self.name) > 0:
            return self.name
        else:
            return "Sector " + str(self.sector_id)

    def __str__(self) -> str:
        return self.gym.abv + " - " + self.pretty_name()


class Orientation(models.Model):
    
    name = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name

class OutdoorSector(Sector):
    crag = models.ForeignKey(Crag, on_delete=models.CASCADE)  # deleting a crag -> delete its sectors
    orientations = models.ManyToManyField(Orientation, blank=True)

    notes = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return self.crag.name + " - " + str(self.name)



class Problem(models.Model):

    class Meta:
        ordering = ["-date_added", "grade"]

    # overall grade of the problem
    # maybe we should put an integer here to be able to compare between different gyms?
    grade = models.CharField(max_length=10)

    # problem settings
    hand_holds = models.ManyToManyField(HandHold, blank=True)
    footwork = models.ManyToManyField(Footwork, blank=True)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.PROTECT)  # PROTECT: cannot remove a problem type unless it is not referenced by any problem
    problem_method = models.ManyToManyField(ProblemMethod, blank=True)

    # Retrieving the problem
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)  # PROTECT: cannot delete a gym that has boulder problems 
    sector = models.ForeignKey(IndoorSector, on_delete=models.PROTECT, blank=True, null=True)  # cannot delete a sector that has problems associated
    date_added = models.DateField(default=datetime.date.today)
    
    # track problem life cycle
    removed = models.BooleanField(default=False)

    def upload_picture(instance, filename):
        _, ext = os.path.splitext(filename)
        return os.path.join('problems', instance._pic_name() + ext)
    
    def picture_display(self):
        from django.utils.html import format_html
        return format_html('<img src="{}" width="400px" height="500px">', self.picture.url)

    picture = models.ImageField(upload_to=upload_picture)

    def description(self):
        return ", ".join(self.hand_holds + self.footwork + self.problem_method)

    def name(self, desc: bool = False):
        name = "{}: {} {}".format(self.sector,
                                  self.grade,
                                  self.problem_type)
        if desc:
            name += " ({})".format(self.description())
        return name

    def rank(self, threshold_positions):
        if not threshold_positions or self.gym not in threshold_positions or len(threshold_positions[self.gym]) == 0:
            return Rank.UNK
        try:
            order = grades_list(self.gym, default=False)
            grade_pos = order.index(self.grade) # position of problem grade in the scale
            positions = threshold_positions[self.gym]
            if grade_pos < positions[0]:
                return Rank.LOWER
            if grade_pos > positions[-1]:
                return Rank.HIGHER
            else:
                return Rank.EXPECT
        except KeyError:
            return Rank.UNK

    def str_repr(self, attr: Union[ProblemMethod, HandHold, Footwork]):
        if attr == ProblemMethod:
            return "|".join(self.problem_method.values_list('name', flat=True))
        elif attr == HandHold:
            return "|".join(self.hand_holds.values_list('name', flat=True))
        elif attr == Footwork:
            return "|".join(self.footwork.values_list('name', flat=True))
        else:
            return ""

    def _pic_name(self):
        return "{}_{}_{}_{}".format(self.gym.abv, self.grade, self.date_added.strftime("%m%y"), rand_name())

    def __str__(self) -> str:
        return self.name()


class RIC(models.Model):
    
    reviewer = models.ForeignKey(Climber, on_delete=models.PROTECT)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # CASCADE: if problem is deleted, comments are deleted
    
    class RICGrade(models.IntegerChoices):
        VERY_LOW = 1
        LOW = 2
        AVERAGE = 3
        HIGH = 4
        VERY_HIGH = 5
    
    risk = models.IntegerField(choices=RICGrade.choices)
    intensity = models.IntegerField(choices=RICGrade.choices)
    complexity = models.IntegerField(choices=RICGrade.choices)

    def average(self):
        return (self.risk + self.intensity + self.complexity) / 3


class Review(models.Model):

    reviewer = models.ForeignKey(Climber, on_delete=models.PROTECT)  # PROTECT: cannot remove a climber who posted reviews
    comment = models.CharField(max_length=120)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # CASCADE: if problem is deleted, comments are deleted

    class Rating(models.IntegerChoices):
        NOT_RATED = 0
        VERY_BAD = 1
        BAD = 2
        AVERAGE = 3
        COOL = 4
        VERY_COOL = 5
    
    rating = models.IntegerField(choices=Rating.choices)
    date = models.DateField(default=datetime.date.today)

    def __str__(self) -> str:
        return "[{}] ({}): {}".format(self.reviewer, self.problem, self.comment)


class Session(models.Model):

    class Meta:
        ordering = ["-date"]
    
    # session info
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)  # PROTECT: cannot remove a gym where sessions took place
    time = models.TimeField()
    date = models.DateField()
    duration = models.DecimalField(max_digits=3, decimal_places=2)  # in hours
    climber = models.ForeignKey(Climber, on_delete=models.PROTECT, related_name="sessions")
    partners = models.ManyToManyField(Climber, related_name="was_at", blank=True)

    # data
    sleep = models.DecimalField("sleeping hours the night before", max_digits=3, decimal_places=1)
    alcohol = models.IntegerField("alcohol consumption the day before")

    # equipments
    shoes = models.ForeignKey(Shoes, on_delete=models.PROTECT)  # PROTECT: cannot remove shoes if used during a session

    # subjective feelings
    notes  = models.CharField(max_length=300)
    
    class Grade(models.IntegerChoices):
        UNKNOWN = -1
        EXECRABLE = 0
        VERY_BAD = 1
        BAD = 2
        SOMEWHAT_BAD = 3
        AVERAGE = 4
        SOMEWHAT_GOOD = 5
        GOOD = 6
        VERY_GOOD = 7
        GREAT = 8
        FANTASTIC = 9
    
    overall_grade = models.IntegerField(choices=Grade.choices)
    strength = models.IntegerField(choices=Grade.choices) 
    motivation = models.IntegerField(choices=Grade.choices)
    fear = models.IntegerField(choices=Grade.choices) 

    def __str__(self) -> str:
        return "{} - {}".format(self.gym, self.date)
    
    def statistics(self):
        ## general data
        # percentage of successes
        tops = self.tops.count()
        fails = self.failures.count() + self.zones.count()
        total = tops + fails
        successes = math.floor(tops * 100/ total) if total > 0 else "??"

        # problems specific data
            # types, grades, holds
        pb_types = defaultdict(lambda: [0,0])
        pb_grades = defaultdict(lambda: [0,0])

        grades = grades_list(self.gym, default=False)
        if grades:
            pb_grades = { elt: [0,0] for elt in grades }
        pb_holds = defaultdict(lambda: [0,0])

        def _add(t, pos: int):
            pb_types[str(t.problem.problem_type)][pos] += 1
            pb_grades[str(t.problem.grade)][pos] += 1
            for hh in t.problem.hand_holds.all():
                pb_holds[str(hh)][pos] += 1

        for t in self.tops.all():
            _add(t, 0)
        for t in itertools.chain(self.failures.all(), self.zones.all()):
            _add(t, 1)

        pb_grades = { k: v for k,v in pb_grades.items() if sum(v) > 0 }

        data = {
            # general data
            "duration": self.duration,
            "grade": self.overall_grade,
            "successes": successes,

            # pb specific
            'problems': {
                'types': pb_types,
                'grades': pb_grades,
                'holds': pb_holds
            }
        }
        return data


class Try(models.Model):

    session = models.ForeignKey(Session, on_delete=models.PROTECT, related_name="%(class)ss")
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, related_name="%(class)ss")
    attempts = models.IntegerField(default=1)
    
    def name(self):
        return self.session.date.strftime("%d/%m/%y") + " " + str(self.problem)

    def pb_grade(self):
        return self.problem.grade

    class Meta:
        abstract = True
        ordering = ["-session__date", "problem__grade"]
    

class Top(Try):

    def __str__(self) -> str:
        start = "[FLASH] - " if self.attempts == 1 else "[TOP] - "
        return start + self.name()


class Failure(Try):
    
    def __str__(self) -> str:
        return "[FAIL] - " + self.name()


class Zone(Try):

    def __str__(self) -> str:
        return "[ZONE] - " + self.name()
