from django.db import models
from django.utils import timezone


class LogDetail(models.Model):
    STATUS_EMAIL = (
        ('PENDING', 'PENDING'),
        ('SENT',  'SENT'),
        ('FAILED', 'FAILED'),
    )
    PRIORITY = (
        ('NORMAL',  'NORMAL'),
        ('HIGH', 'HIGH'),
    )

    email = models.CharField('Email',max_length=50)
    timestamp_created = models.DateTimeField('Created Time', default=timezone.now())
    timestamp_updated = models.DateTimeField(default=timezone.now())
    timestamp_delivered_email = models.DateTimeField(blank=True,null=True)
    email_subject = models.TextField(max_length=50,default=0)
    email_content = models.TextField(max_length=1000,default=0)
    trial_no_email = models.IntegerField(default=0)  # TOTAL NUMBER OF EMAIL SENDING ATTEMPTS ALREADY DONE
    email_response = models.TextField('Email Response', default='PLACEHOLDER_RESPONSE')
    status_email=models.CharField('Email Status',max_length=8,
                                   choices=STATUS_EMAIL,null=True,blank=True)
    created_by = models.CharField(max_length=50,default=0)
    meta_text = models.TextField(max_length=500,default=0) # not used
    source_project = models.CharField(max_length=50,default="TAB")
    priority = models.CharField(max_length=13,
                            choices = PRIORITY,
                            default='NORMAL',null=True,blank=True)
    type = models.CharField(max_length=50, default=0)

    def __unicode__(self):
        return str(self.id)
