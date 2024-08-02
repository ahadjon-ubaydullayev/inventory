from django.contrib import admin
from .models import ElectrodeLabel, ElectrodeCategory, Electrode, ElectrodeHistory
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ElectrodeLabelAdmin(admin.ModelAdmin):
    list_display = ['label_name']
    search_fields = ['label_name']


class ElectrodeCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    search_fields = ['category_name']


class ElectrodeAdmin(admin.ModelAdmin):
    list_display = ['label', 'category', 'package',
                    'box', 'weight', 'added_date']
    search_fields = ['label__label_name', 'category__category_name', 'package',
                     'box', 'weight', 'count_by_label', 'added_date', 'description']


class ElectrodeHistoryAdmin(admin.ModelAdmin):
    list_display = ('electrode', 'transaction_type',
                    'quantity', 'customer', 'timestamp')
    search_fields = ('electrode__label__label_name',
                     'customer__name', 'transaction_type')


admin.site.register(ElectrodeLabel, ElectrodeLabelAdmin)
admin.site.register(ElectrodeCategory, ElectrodeCategoryAdmin)
admin.site.register(Electrode, ElectrodeAdmin)
admin.site.register(ElectrodeHistory, ElectrodeHistoryAdmin)
