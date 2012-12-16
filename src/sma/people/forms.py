# -*- coding: utf-8 -*-
from django import forms
from sma.people.models import SarparastiProfile

class SarparastiProfileForm(forms.ModelForm):
    class Meta:
        model = SarparastiProfile
        exclude = ('member',)
