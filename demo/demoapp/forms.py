from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from demoapp.models import UserProfile


class AuthenticationForm(forms.Form):
    username = forms.EmailField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'id': "id_user_password"}))
    retype_password = forms.CharField(min_length=6, widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        exclude = ('user', 'registration_type', 'is_email_verified')

    def clean_email(self):
        user = None
        cleaned_data = super(UserRegistrationForm, self).clean()
        email = cleaned_data.get('email').lower()
        try:
            user = User.objects.get(email=email)
        except:
            pass
        if user:
            raise forms.ValidationError("This email ID is already registered with us.")
        return email

    def clean_retype_password(self):
        print"this worked for brand form validation"
        cleaned_data = super(UserRegistrationForm, self).clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("retype_password")
        print "password", password1
        print "retyped password", password2

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2