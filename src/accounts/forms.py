from django import forms
from django.dispatch import receiver
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.signals import user_signed_up
from .models import MyUser

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    
    It will replace default creation form for creating new user
    """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email',
                  'password',
                  'first_name',
                  'last_name',
                  'is_active',
                  'is_admin',
                  'is_member')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget=forms.TextInput(
                                   attrs={'placeholder':
                                          (''),
                                          'autofocus': 'autofocus'})
        self.fields['password'].widget = forms.PasswordInput()
        # You don't want the `remember` field?
        if 'remember' in self.fields.keys():
            del self.fields['remember']


class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget=forms.TextInput(
                                   attrs={'placeholder':
                                          (''),
                                          'autofocus': 'autofocus'})
        self.fields['email'].widget=forms.TextInput(
                                   attrs={'placeholder':
                                          (''),
                                          'autofocus': 'autofocus'})
        self.fields['password1'].widget = forms.PasswordInput()

        self.fields['password2'].widget = forms.PasswordInput()



@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    # user signed up now send email
    # send email part - do your self
    print("new user")