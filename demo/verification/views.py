from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail

from demoapp.models import UserProfile
from .models import EmailVerification

chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

@login_required()
def resend_email(request):
    print "resend mail view"
    print request.user
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    if user_profile and user_profile.is_email_verified==False:
        print "email not verified yet"
        try:
            email_verify_object = EmailVerification.objects.get(user=user_profile, entry_valid=True)
        except:
            email_verify_object = None
        if email_verify_object:
            print "email obj found"
            email_verify_object.entry_valid = False
            email_verify_object.save()
            email_verify_object = EmailVerification()
            email_verify_object.user = user_profile
            email_verify_object.email = str(user_profile.user.email)
            email_verify_object.verification_key = get_random_string(20, chars)
            email_verify_object.save()

            # Below task will be made to run in background using celery
            # Verification Email sending code. Will be using django templated email.
            try:
                from django.contrib.sites.models import Site
                site = Site.objects.get_current()
                send_mail('Demo App - Confirm Email', 'Please click here'+str("http://"+str(site.domain)+"registration/confirm-email/"+email_verify_object.verification_key)+'/', 'askar@demoapp.com',
                                            [user_profile.user.email], fail_silently=False)

            except:
                pass

            messages.success(request,"Verification mail has been resent.")
        return HttpResponseRedirect('/profile')
    else:
        return HttpResponseRedirect('/dashboard')


def email_confirmation(request, key=None):
    print "email confirmation page"
    try:
        email_confirmation_object = EmailVerification.objects.get(verification_key=key, entry_valid=True)
    except:
        print "except"
        email_confirmation_object = None

    if email_confirmation_object:
        user_profile = email_confirmation_object.user
        user_profile.is_email_verified = True
        user_profile.save()
        email_confirmation_object.entry_valid = False
        email_confirmation_object.save()
        print "saved email cofirm obj"
        messages.success(request, "Email successfully verified.")
    return HttpResponseRedirect('/')
