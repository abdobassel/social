from django import forms
from django_countries.widgets import CountrySelectWidget

from .models import Profile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_photo", "bio", "country", "city", "phone_number"]
        widgets = {"country": CountrySelectWidget()}
