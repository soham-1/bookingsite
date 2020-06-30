from django.contrib import admin
from .models import Auditorium, TimeSlot, Event

# Register your models here.
admin.site.register(Auditorium)
admin.site.register(TimeSlot)
admin.site.register(Event)