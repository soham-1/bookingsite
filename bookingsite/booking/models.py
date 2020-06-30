from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from multiselectfield import MultiSelectField
import os

# Create your models here.

def add_to_default_group(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        group = Group.objects.get(name='student')
        user.groups.add(group)

post_save.connect(add_to_default_group, sender=User)


class Auditorium(models.Model):
    name = models.CharField(max_length=100, blank=True, primary_key=True)
    img = models.ImageField(upload_to='booking/images', default='booking/images/blank.png') # creates folder in media directory....default must be added manually
    # in that folder after entering a first data
     
    description = models.CharField(max_length=255, blank=True)

    def filename(self):  # represent the file with file name in database
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednessday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday')
    )
    audiname = models.ForeignKey(Auditorium, on_delete=models.CASCADE, to_field='name')
    start_at = models.TimeField(null=True, blank=True)
    close_at = models.TimeField(null=True, blank=True)
    days = MultiSelectField(choices=DAY_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = (('audiname', 'start_at', 'close_at', 'days'),)

    def __str__(self):
        return str(self.audiname)+str(self.days)

class Event(models.Model):
    email = models.CharField(max_length=250, null=True, blank=True)
    eventname = models.CharField(max_length=200, null=True, blank=True)
    eventdesc = models.CharField(max_length=300, null=True, blank=True)
    eventdate = models.DateField(null=True, blank=True)
    slots = models.TimeField(null=True, blank=True)
    eventexp = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    status = models.SmallIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.eventname