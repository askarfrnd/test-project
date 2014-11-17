from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" %(uuid.uuid4(), ext)
        upload_path = 'uploads/'+str(instance.user_profile.user.username)+'/'+str(instance.__class__.__name__).lower()
        return os.path.join(upload_path, filename)


class UserProfile(models.Model):
    REGISTRATION_TYPE = (
        ('NORMAL', 'NORMAL'),
        ('SOCIAL', 'SOCIAL'),
    )

    user = models.OneToOneField(User, related_name='user_profile')
    name = models.CharField(max_length=255)
    registration_type = models.CharField(max_length=10, choices=REGISTRATION_TYPE, default="SOCIAL", null=True)
    is_email_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name