"""
This is the database model for the Bungalow coding Challenge

- using abitrary CharField max_length values but in a PostgreSQL database
  I would use Text field since it has been made more efficient than varchar
-
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


# Create your models here.
class Listing(models.Model):
    # allow for larger integers as these could grow very large
    id = models.BigIntegerField(primary_key=True)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    # PositiveIntegerField allows 0 which is a valid ZIPCODE (although lowest seems to be 00501
    # disallow adding value of 5-digit zipcode (this is not made for Canada)
    zipcode = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999)]
    )
    area_unit = models.CharField(max_length=100)
    property_size = models.PositiveIntegerField()
    # TODO should this be a choices list? what are valid choices?
    # are all the valid choices in the sample? This is why it is open right now
    property_type = models.CharField('type', max_length=100)
    # XXX should this be auto-generated?
    link = models.URLField()
    price = models.PositiveIntegerField()
    property_size = models.PositiveIntegerField()
    tax_value = models.PositiveIntegerField()
    tax_year = models.PositiveIntegerField()


class Rent(models.Model):
    # allow multiple estimates for a given property (we will only show last)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True)
    estimate_amount = models.PositiveIntegerField()
    estimate_date = models.DateField(auto_now=True)


class Sale(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField('last sold price', null=True)
    date = models.DateField('last sold date', auto_now=True)


class Estimate(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    estimate_amount = models.PositiveIntegerField()
    estimate_date = models.DateField(auto_now=True)


class Building(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    area_unit = models.CharField(max_length=100)
    bathrooms = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    year_build = models.PositiveIntegerField()
