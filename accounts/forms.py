from django import forms
from .models import *

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ("email", "phone", "other_achievements", "skills_abilities", "interests", "public")

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        exclude = ("cv",)

class AddressCVForm(forms.ModelForm):
    class Meta:
        model = AddressCV
        exclude = ("cv",)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ("cv",)

class TechSkillForm(forms.ModelForm):
    class Meta:
        model = TechSkill
        exclude = ("cv",)

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ("cv",)

class AddressRefereeForm(forms.ModelForm):
    class Meta:
        model = AddressReferee
        exclude = ("cv",)
