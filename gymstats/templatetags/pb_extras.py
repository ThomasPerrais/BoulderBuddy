from django import template
from gymstats.models import Problem


register = template.Library()

@register.filter(name="display")
def problem_title(pb: Problem): 
    """
    Display function used as title for a Problem
    """
    return "{} - {} {} ({})".format(pb.grade, pb.gym.brand, pb.gym.city, pb.date_added.strftime("%d/%m/%y"))


@register.filter(name="gallery_display")
def problem_gallery_title(pb: Problem):
    return "{} - {}".format(pb.grade, pb.sector);


@register.filter(name="fw")
def problem_fw(pb: Problem):
    for fw in pb.footwork.all():
        yield fw

@register.filter(name="hh")
def problem_hh(pb: Problem):
    for hh in pb.hand_holds.all():
        yield hh

@register.filter(name="me")
def problem_hh(pb: Problem):
    for me in pb.problem_method.all():
        yield me