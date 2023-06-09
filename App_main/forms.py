from django import forms
from .models import *


class BMIForm(forms.ModelForm):
    class Meta:
        model = BMIModel
        fields = ['height', 'weight', 'age', 'sex']


class WorkoutPlanModelForm(forms.ModelForm):
    duration = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': ' (in minutes)'}))

    class Meta:
        model = WorkoutPlanModel
        fields = ['duration', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        widgets = {
            'sunday': forms.CheckboxSelectMultiple(),
            'monday': forms.CheckboxSelectMultiple(),
            'tuesday': forms.CheckboxSelectMultiple(),
            'wednesday': forms.CheckboxSelectMultiple(),
            'thursday': forms.CheckboxSelectMultiple(),
            'friday': forms.CheckboxSelectMultiple(),
            'saturday': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].queryset = Workout.objects.all()

    def save(self, profile, member, commit=True):
        instance = super().save(commit=False)
        instance.trainer = profile
        instance.trainee = member
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class DietChartModelForm(forms.ModelForm):
    class Meta:
        model = DietChartModel
        fields = ['sunday_breakfast', 'sunday_lunch', 'sunday_dinner', 'sunday_snacks',
                  'monday_breakfast', 'monday_lunch', 'monday_dinner', 'monday_snacks',
                  'tuesday_breakfast', 'tuesday_lunch', 'tuesday_dinner', 'tuesday_snacks',
                  'wednesday_breakfast', 'wednesday_lunch', 'wednesday_dinner', 'wednesday_snacks',
                  'thursday_breakfast', 'thursday_lunch', 'thursday_dinner', 'thursday_snacks',
                  'friday_breakfast', 'friday_lunch', 'friday_dinner', 'friday_snacks',
                  'saturday_breakfast', 'saturday_lunch', 'saturday_dinner', 'saturday_snacks']

