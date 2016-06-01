from django import forms

from accounts.models import MyUser

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5}))
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = MyUser.objects.get(email = self.request.user.email).email
        
