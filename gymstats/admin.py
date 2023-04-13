from django.contrib import admin
from .models import Problem, ProblemMethod, ProblemType, HandHold, Footwork, Gym, Climber
from .models import Shoes, ShoesFixing, Session, Top, Failure, Zone, Review  # ideally those should be removed once views are written


# Register your models here.
admin.site.register(Problem)
admin.site.register(ProblemType)
admin.site.register(ProblemMethod)
admin.site.register(HandHold)
admin.site.register(Footwork)
admin.site.register(Gym)
admin.site.register(Climber)

admin.site.register(Shoes)
admin.site.register(ShoesFixing)
admin.site.register(Session)
admin.site.register(Top)
admin.site.register(Zone)
admin.site.register(Failure)
admin.site.register(Review)