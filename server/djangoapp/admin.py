from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    fields = ("name", "dealer_id", "type", "year")
    show_change_link = True

class CarMakeAdmin(admin.ModelAdmin):
    list_display   = ("name", "description")
    search_fields  = ("name",)
    inlines        = [CarModelInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display   = ("name", "car_make", "dealer_id", "type", "year")
    list_filter    = ("car_make", "type", "year")
    search_fields  = ("name", "car_make__name")
    ordering       = ("car_make", "year", "name")

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)