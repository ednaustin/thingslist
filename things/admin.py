from django.contrib import admin
from .models import Things

class ThingsAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Things, ThingsAdmin)
