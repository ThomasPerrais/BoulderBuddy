from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm, Textarea
from django.forms.utils import ErrorList
from gymstats.models import Session, Climber, Problem, Try
from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, HTML, Submit, Button
from crispy_forms.bootstrap import AppendedText, PrependedAppendedText, PrependedText, FormActions



class ClimberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'General',
                Row(
                    Column(PrependedText('name', '👤'), css_class="form-group ml-3 mr-4"),
                    Column(PrependedText('picture', '🏢'), css_class="form-group mb-1 mr-3"),
                )
            ),
            Fieldset(
                'Preferences',
                Row(
                    # Column(PrependedText("stats_preference", "📅"), css_class="mr-2"),
                    Column(PrependedText("month_hard_boulder_target", "🕒"), css_class="mr-2"),
                    Column(AppendedText('month_hour_target', "h"))
                )
            ),
            Fieldset(
                'Gyms',
                Column(PrependedText("preferred_gyms", ""), css_class="mr-2"),
            ),
            FormActions(
                Submit('save', 'Save changes', css_class="btn btn-light"),
                Button('cancel', 'Cancel')
            ),
        )

    class Meta:
        model = Climber
        fields = ["name", "picture", "month_hard_boulder_target", "month_hour_target", "preferred_gyms"]


class SessionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'General',
                Row(
                    Column(PrependedText('climber', '👤'), css_class="form-group ml-3 mr-4"),
                    Column(PrependedText('gym', '🏢'), css_class="form-group mb-1 mr-3"),
                ),
                Column("partners", css_class="form-group"),
            ),
            Fieldset(
                'Time',
                Row(
                    Column(PrependedText("date", "📅"), css_class="mr-2"),
                    Column(PrependedText("time", "🕒"), css_class="mr-2"),
                    Column(AppendedText('duration', "h"))
                )
            ),
            Fieldset(
                'Data',
                PrependedText("shoes", "👟"),
                Row(
                    Column(PrependedText("sleep", "🛏️")),
                    Column(PrependedText("alcohol", "🍺")),
                )
            ),
            Fieldset(
                'Feelings',
                PrependedText("notes", "🗈"),
                PrependedText("overall_grade", "⭐"),
                Row(
                    Column(PrependedText("strength", "💪"), css_class="mr-2"),
                    Column(PrependedText("motivation", "🔥"), css_class="mr-2"),
                    Column(PrependedText('fear', "😨"))
                )
            ),
            FormActions(
                Submit('save', 'Save changes', css_class="btn btn-light"),
                Button('cancel', 'Cancel')
            ),
        )

    class Meta:
        model = Session
        fields = '__all__'

        widget = {
            "notes": Textarea(attrs={"cols": 150, "rows": 40}),
        }


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

