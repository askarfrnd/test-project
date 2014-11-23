from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, get_user_model
from django.template import loader

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
        exclude = ('user', 'is_email_verified')

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


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'is_email_verified')