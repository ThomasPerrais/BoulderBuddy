from django import template
from gymstats.models import Session


register = template.Library()

@register.filter(name="title")
def session_title(sess: Session): 
    """
    Display function used as title for a Problem
    """
    return "{} : {} {}".format(sess.date.strftime("%d/%m/%Y"), sess.gym.brand, sess.gym.city)
