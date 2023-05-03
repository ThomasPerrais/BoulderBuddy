from django import template
from gymstats.models import Problem


register = template.Library()

@register.filter(name="display")
def problem_title(pb: Problem): 
    """
    Display function used as title for a Problem
    """
    return "{} - {} {} ({})".format(pb.grade, pb.gym.brand, pb.gym.city, pb.date_added.strftime("%d/%m/%y"))
