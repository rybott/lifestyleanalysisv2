from django import forms
from django.forms import ModelForm
from .models import Net_kcal, Activity

# Create Net_kcal form
class kCalForm(ModelForm):
    class Meta:
        model = Net_kcal
        fields = ('date','cal_in','cal_out_apple','cal_out_app')
        