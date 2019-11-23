from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    comment = forms.CharField(
        label='리뷰',
        
    score = models.IntegerField()