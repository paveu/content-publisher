from django import forms

class UpgradePayuForm(forms.Form):
    description = forms.CharField(required=True, initial='Message to admin')
