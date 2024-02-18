from django.contrib import admin
from .models import TruckModel
from .utils import calculate_distance


class TruckModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'rel_distance']
    actions = ['calculate_rel_distance']

    def calculate_rel_distance(self, request, queryset):
        for obj in queryset:
            dis = calculate_distance(obj.locationx, obj.locationy)
            obj.rel_distance = dis
            obj.save()

    calculate_rel_distance.short_description = "Calculate Relative Distance"

# Register your models here.


admin.site.register(TruckModel, TruckModelAdmin)
