from django.db import models
import datetime
from typing import Any
import os
import random


class Gym(models.Model):
    """
    Gym model represents a climbing gym where a Session takes place.
    Climbing gyms with both lead climbing and bouldering should be split in 2 instances
    """
    location = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    abv = models.CharField(max_length=10)

    class GymType(models.TextChoices):
        BOULDER = 'Boulder'
        LEAD = 'Lead'

    gym_type = models.CharField(max_length=10, choices=GymType.choices, default=GymType.BOULDER)

    def __str__(self) -> str:
        return "{} {} ({})".format(self.brand, self.location, self.gym_type)


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


class Climber(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


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


class ProblemType(Describable):  # choices: [vertical, slab, overhanging]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('problem-type', *args, **kwargs)


class ProblemMethod(Describable):  # choices: [dyno, coordo, lolotte, flex, mantle]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__('problem-method', *args, **kwargs)


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
    date_added = models.DateField(default=datetime.date.today)
    
    def upload_picture(instance, filename):
        _, ext = os.path.splitext(filename)
        return os.path.join('problems', instance._pic_name() + ext)
    
    picture = models.ImageField(upload_to=upload_picture)

    def description(self):
        return ", ".join(self.hand_holds + self.footwork + self.problem_method)

    def name(self, desc: bool = False):
        name = "{} {}: {} {}".format(self.gym.abv,
                                     self.date_added.strftime("%b. %y"),
                                     self.grade,
                                     self.problem_type)
        if desc:
            name += " ({})".format(self.description())
        return name

    def _pic_name(self):
        def _rand_id():
            return "".join([chr(random.randint(97, 122)) for _ in range(5)])
        return "{}_{}_{}_{}".format(self.gym.abv, self.grade, self.date_added.strftime("%m%y"), _rand_id())

    def __str__(self) -> str:
        return self.name()


class Review(models.Model):

    reviewer = models.ForeignKey(Climber, on_delete=models.PROTECT)  # PROTECT: cannot remove a climber who posted reviews
    comment = models.CharField(max_length=120)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # CASCADE: if problem is deleted, comments are deleted

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


class Try(models.Model):

    session = models.ForeignKey(Session, on_delete=models.PROTECT, related_name="%(class)ss")
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, related_name="%(class)ss")
    attempts = models.IntegerField(default=1)
    
    def name(self):
        return self.session.date.strftime("%d/%m/%y") + " " + str(self.problem)

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
