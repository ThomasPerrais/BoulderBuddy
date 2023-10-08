from django import template
from gymstats.models import IndoorProblem


register = template.Library()

@register.filter(name="display")
def problem_title(pb: IndoorProblem): 
    """
    Display function used as title for a Problem
    """
    return "{} - {} {} ({})".format(pb.grade, pb.gym.brand, pb.gym.city, pb.date_added.strftime("%d/%m/%y"))


@register.filter(name="gallery_display")
def problem_gallery_title(pb: IndoorProblem):
    return "{} - {}".format(pb.grade, pb.sector);


@register.filter(name="fw")
def problem_fw(pb: IndoorProblem):
    for fw in pb.footwork.all():
        yield fw

@register.filter(name="hh")
def problem_hh(pb: IndoorProblem):
    for hh in pb.hand_holds.all():
        yield hh

@register.filter(name="me")
def problem_mv(pb: IndoorProblem):
    for me in pb.moves.all():
        yield me