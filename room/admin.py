from django.contrib import admin

from .models import *


class TimeFieldAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)


admin.site.register(Room)
admin.site.register(Message, TimeFieldAdmin)
