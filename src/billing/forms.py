from django import forms
from django.conf import settings



class UpgradePayuForm(forms.Form):
    amount =  forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly':'True'}), initial=settings.TOTAL_AMOUNT)
    description = forms.CharField(required=True, initial='Message to admin')