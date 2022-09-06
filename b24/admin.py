from django.contrib import admin
from .models import Region, Partner, DemoRequest

admin.site.register(Region)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'get_regions')


class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'email', 'request_date', 'region', 'partner')


admin.site.register(Partner, PartnerAdmin)
admin.site.register(DemoRequest, DemoRequestAdmin)

# Register your models here.
