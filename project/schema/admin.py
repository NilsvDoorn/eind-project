from django.contrib import admin
from .models import Rooms, Booked, Reviews, Cleanshifts

# Register your models here.
admin.site.register(Rooms)
admin.site.register(Booked)
admin.site.register(Reviews)
admin.site.register(Cleanshifts)
