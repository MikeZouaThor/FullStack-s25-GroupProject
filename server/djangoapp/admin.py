from django.contrib import admin
from .models import CarMake, CarModel





class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display for adding new models

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]  


admin.site.register(CarMake)
admin.site.register(CarModel)


