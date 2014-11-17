from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    name = models.CharField(max_length=255)
    is_email_verified = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name