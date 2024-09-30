from django.contrib import admin
from . import models

class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status')
    search_fields = ('username', 'email')
    list_filter = ('status',)

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.ProductType)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.HelpRequest,HelpRequestAdmin)