
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make= models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    types= models.CharField(
        max_length=20,
        choices=[
            ('SEDAN', 'Sedan'),
            ('SUV', 'SUV'),
            ('WAGON', 'Wagon'),
            ('COUPE', 'Coupe'),
            ('CONVERTIBLE', 'Convertible'),
            ('HATCHBACK', 'Hatchback'),
            ('PICKUP', 'Pickup'),
            ('VAN', 'Van'),
            ('SPORTS', 'Sports'),
            ('LUXURY', 'Luxury'),
            ('ELECTRIC', 'Electric'),
            ('HYBRID', 'Hybrid'),
            ('TURBO', 'Turbo'),
            ('DIESEL', 'Diesel'),
            ('CROSSOVER', 'Crossover'),
            ('MINIVAN', 'Minivan'),
            ('OFFROAD', 'Offroad'),
            ('OTHER', 'Other'),],
        default='SEDAN'
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(2010),
            MaxValueValidator(2023)
        ]
    )
    def __str__(self):
        return f"{self.name} ({self.year}) - {self.make.name}"
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
