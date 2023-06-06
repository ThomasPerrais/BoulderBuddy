from django.forms import ModelForm
from gymstats.models import Session, Climber, Sector, Problem, Try
from django import forms
from dal import autocomplete


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ["gym", "time", "date", "climber", "partners"]


class TryForm(ModelForm):
    class Meta:
        model = Try
        exclude = ()
        widgets = {
            'problem': autocomplete.ModelSelect2(url='gs:problem-autocomplete',
                                                attrs={'data-html': True},
                                                forward=['sector', 'gym', 'session']),
        }

class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        exclude = ("removed",)
        widgets = {
            'sector': autocomplete.ModelSelect2(url='gs:sector-autocomplete',
                                                attrs={'data-html': True},
                                                forward=['gym']),
            'gym': autocomplete.ModelSelect2(url="gs:gym-autocomplete"),
            'grade': autocomplete.Select2(url='gs:grade-autocomplete',
                                                forward=['gym'])
        }

