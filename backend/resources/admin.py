from django.contrib import admin

from resources.models import DayAvailability, Resource

# Register your models here.
admin.site.register(DayAvailability)
admin.site.register(Resource)
