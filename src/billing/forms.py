from django import forms

class UpgradePayuForm(forms.Form):
    description = forms.CharField(required=True, initial='Premium membership')
