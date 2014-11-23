from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from demoapp.models import UserProfile


class EmailVerification(models.Model):
    user = models.ForeignKey(UserProfile)
    email = models.EmailField('Existing Email', max_length=75)
    verification_key = models.CharField('Verification Key', max_length=255)
    issued_at = models.DateTimeField('Issued at', default=timezone.now())
    entry_valid = models.BooleanField('Valid Entry', default=True)
    attempts = models.IntegerField('Total Attempts', default=0)
    email_send = models.BooleanField('Email Send', default=False)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email_expired_after = datetime.now()+timedelta(days=1)
        super(EmailVerification, self).save(*args, **kwargs)
