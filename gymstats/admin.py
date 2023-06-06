from django.contrib import admin
from django.utils.html import format_html
from .forms import ProblemForm, TryForm
from .models import Problem, ProblemMethod, ProblemType, HandHold, Footwork, Gym, Sector, Climber
from .models import Shoes, ShoesFixing, Session, Top, Failure, Zone, Review, RIC  # ideally those should be removed once views are written


class TopInline(admin.TabularInline):
    form = TryForm
    model = Top
    extra = 5

class ZoneInline(admin.TabularInline):
    form = TryForm
    model = Zone
    extra = 3

class FailureInline(admin.TabularInline):
    form = TryForm
    model = Failure
    extra = 3

class RICInline(admin.TabularInline):
    model = RIC
    extra = 1

class SessionAdmin(admin.ModelAdmin):
    list_display = ('gym', 'date', 'climber')
    fieldsets = [
        (None, {'fields': ['gym', 'climber', 'partners']}),
        ('Time', {'fields': ['date', 'time', 'duration']}),
        ('Data', {'fields': ['shoes', 'sleep', 'alcohol']}),
        ('Feelings', {'fields': ['notes', 'overall_grade', 'strength', 'motivation', 'fear']}),
    ]
    inlines = [TopInline, ZoneInline, FailureInline]


class ProblemAdmin(admin.ModelAdmin):

    form = ProblemForm
    list_filter = ['gym__abv', 'grade', 'removed', 'problem_type', 'hand_holds']
    list_display = ('gym', 'grade', 'picture', 'removed')
    list_editable = ("removed",)

    readonly_fields = ["picture_display"]
    fieldsets = [
        ('General', {'fields': ["gym", "grade", "sector", "date_added"]}),
        ('Picture', {'fields': ["picture", "picture_display"]}),
        ('Details', {'fields': ["problem_type", "hand_holds", "footwork", "problem_method"]}),
    ]
    inlines = [RICInline]


class TryAdmin(admin.ModelAdmin):
    form = TryForm
    list_display = ('session', 'pb_grade', 'attempts')


# Register your models here.
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemType)
admin.site.register(ProblemMethod)
admin.site.register(HandHold)
admin.site.register(Footwork)
admin.site.register(Gym)
admin.site.register(Sector)
admin.site.register(Climber)

admin.site.register(Shoes)
admin.site.register(ShoesFixing)
admin.site.register(Session, SessionAdmin)
admin.site.register(Top, TryAdmin)
admin.site.register(Zone, TryAdmin)
admin.site.register(Failure, TryAdmin)
admin.site.register(Review)
admin.site.register(RIC)