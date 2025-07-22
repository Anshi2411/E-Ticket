from django import forms
from .models import UserProfile

class YourProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_image',
            'mobile',
            'gender',
            'occupation'
        ]

class RechargeForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
