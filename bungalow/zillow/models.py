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

    # housing information which may be null (as land does not have a structure)
    # did not put into a separate table as there is no need to have a 1-N
    # relationship so it should be more efficient to just have a larger
    # table set returned
    bathrooms = models.FloatField(null=True)
    bedrooms = models.FloatField(null=True)
    size = models.PositiveIntegerField(null=True)
    year_build = models.PositiveIntegerField(null=True)
    # useful for ordering purposes
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}/{}".format(self.bedrooms, self.bathrooms)

    @property
    def current_price(self):
        return self.price_set.order_by('-date').first()

    @property
    def latest_tax(self):
        return self.tax_set.order_by('-date').first()

    @property
    def current_rent(self):
        return self.rent_set.order_by('-date').first()

    @property
    def current_rent_estimate(self):
        return self.rent_estimate_set.order_by('-estimate_date').first()

    @property
    def last_sale(self):
        return self.sale_set.order_by('-date').first()

    @property
    def sales(self):
        return self.sale_set.order_by('-date')

    @property
    def zestimate(self):
        return self.estimate_set.order_by('-estimate_date').first()

    def __str__(self):
        return "{}, {}, {}, {:05d}".format(
            self.address,
            self.city,
            self.state,
            self.zipcode,
        )


class Price(models.Model):
    # allow prices for historical information in the future
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "${:,.2f} ({})".format(self.price, self.date)


class Tax(models.Model):
    # allow for historical tax data in the future
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    tax_value = models.FloatField()
    tax_year = models.PositiveIntegerField()

    def __str__(self):
        return "{} ({})".format(self.tax_value, self.tax_year)


class Rent(models.Model):
    # allow historical actual rent information
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "${:,.2f} ({})".format(self.price, self.date)


class RentEstimate(models.Model):
    # allow multiple estimates for a given property (we will only show last)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    estimate_amount = models.PositiveIntegerField()
    estimate_date = models.DateField(auto_now=True)

    def __str__(self):
        return "${:,.2f} ({})".format(self.estimate_amount, self.estimate_date)


class Sale(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField('last sold price', null=True)
    date = models.DateField('last sold date', auto_now=True)

    def __str__(self):
        return "${:,.2f} ({})".format(self.price, self.date)


class Estimate(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    estimate_amount = models.PositiveIntegerField()
    estimate_date = models.DateField(auto_now=True)

    def __str__(self):
        return "${:,.2f} ({})".format(self.estimate_amount, self.estimate_date)
