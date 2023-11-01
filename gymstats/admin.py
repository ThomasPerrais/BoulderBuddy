from django.contrib import admin
from django.utils.html import format_html
from .forms import IndoorBoulderForm, TryForm, SessionForm
from .models import ClimbingMove, WallAngle, HandHold, Footwork, ClimbAttribute, ClimbType
from .models import IndoorSector, OutdoorSector, Gym, Crag, IndoorBoulder, Crux, Climbable
from .models import Climber, HardBoulderThreshold
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

class HardBoulderInline(admin.TabularInline):
    model = HardBoulderThreshold
    extra = 1


class CruxInline(admin.TabularInline):
    # form = ClimbableCruxForm
    model = Crux
    extra = 1


# class ClimbableInline(admin.StackedInline):
#     model = Climbable
#     inlines = [CruxInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    # form = SessionForm
    fieldsets = [
        ('General', {'fields': ['gym', 'climber', 'partners']}),
        ('Time', {'fields': ['date', 'time', 'duration']}),
        ('Data', {'fields': ['shoes', 'sleep', 'alcohol']}),
        ('Feelings', {'fields': ['notes', 'overall_grade', 'strength', 'motivation', 'fear']})
    ]
    list_display = ('gym', 'date', 'climber')
    inlines = [TopInline, ZoneInline, FailureInline]


@admin.register(IndoorBoulder)
class IndoorBoulderAdmin(admin.ModelAdmin):

    form = IndoorBoulderForm
    list_filter = ['sector__gym__abv', 'climbable__grade', 'removed', 'climbable__wall_angle', 'hand_holds']
    list_display = ('sector', 'grade', 'picture', 'removed')
    list_editable = ("removed",)

    fieldsets = [
        ('General', {'fields': ["sector__gym", "climbable__grade", "sector", "date_added"]}),
        ('Picture', {'fields': ["climbable__picture"]}),
        ('Details', {'fields': ["climbable__wall_angle", "hand_holds", "footwork", "climbable__moves"]}),
    ]
    inlines = [RICInline]

    def grade(self, obj):
        return obj.climbable.grade

    def picture(self, obj):
        return obj.climbable.picture


@admin.register(Top, Zone, Failure)
class TryAdmin(admin.ModelAdmin):
    form = TryForm
    list_display = ('session', 'pb_grade', 'attempts')


@admin.register(Climber)
class ClimberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ["user", "name", "picture"]}),
        ('Preferences', {'fields': ["preferred_gyms", "stats_preference", "month_hour_target", "month_hard_boulder_target"]}),
    ]
    inlines = [HardBoulderInline]

# Register your models here.
admin.site.register(WallAngle)
admin.site.register(ClimbingMove)
admin.site.register(ClimbAttribute)
admin.site.register(ClimbType)
admin.site.register(HandHold)
admin.site.register(Footwork)
admin.site.register(Gym)
admin.site.register(Crag)
admin.site.register(IndoorSector)
admin.site.register(OutdoorSector)

admin.site.register(Shoes)
admin.site.register(ShoesFixing)
admin.site.register(Review)
admin.site.register(RIC)