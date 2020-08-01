import csv
import codecs
from datetime import datetime
from . import models


CURRENCY_MAP = {
    'K': 1000,
    'M': 1000000,
    'B': 1000000000,
}



def _get_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, '%m/%d/%Y')


def _convert_price(price_str):
    if not price_str:
        return None
    unit = ''
    if price_str[-1].isalpha():
        unit = price_str[-1]
        price_str = price_str[:-1]
    # TODO handle different currencies
    # remove currency (assume it is all the same)
    currency = '$'
    if not price_str[0].isnumeric():
        currency = price_str[0]
        price_str = price_str[1:]
    price = float(price_str)
    multiplier = CURRENCY_MAP.get(unit)
    if multiplier:
        price *= multiplier
    return int(price)


def ingest_data(uploaded_file):
    # TODO
    # - protect against invalid file here and return proper error
    # - protect against missing headers
    csv_reader = csv.DictReader(codecs.iterdecode(uploaded_file,'utf-8'))
    for row in csv_reader:
        # for simplicity create an object to update/create listing object
        listing_data = {
            'id': row['zillow_id'],
            'address': row['address'],
            'city': row['city'],
            'state': row['state'],
            'zipcode': int(row['zipcode']),
            'area_unit': row['area_unit'],
            'property_size': row['property_size'] and int(row['property_size']) or 0,
            'property_type': row['home_type'],
            'link': row['link'],
            'bathrooms': row['bathrooms'] and float(row['bathrooms']) or None,
            'bedrooms': row['bedrooms'] and float(row['bedrooms']) or None,
            'size': row['home_size'] and int(row['home_size']) or None,
            'year_build': row['year_built'] and int(row['year_built']) or None,
        }
        # assume that we want to update the current listing if already present
        listing, created = models.Listing.objects.update_or_create(
            pk=row['zillow_id'],
            **listing_data,
        )
        # we can now save as we have a complete listing, we can fill
        # in the optional related data now
        listing.save()
        if 'price' in row:
            price = _convert_price(row['price'])
            # do not add a new price if this is the same
            if not listing.price_set.filter(price=price):
                listing.price_set.create(price=price)

        tax_year = row.get('tax_year')
        tax_value = row.get('tax_value')
        # XXX if not present or only one present we are going to ignore
        # for now as we do not create a row if the data isn't valid
        if tax_year and tax_value:
            tax_year = int(tax_year)
            tax_value = float(tax_value)
            if not listing.tax_set.filter(tax_year=tax_year):
                listing.tax_set.create(tax_value=tax_value, tax_year=tax_year)

        # only add if this is new rent value
        rent = _convert_price(row.get('rent', ''))
        if rent and not listing.rent_set.filter(price=rent):
            listing.rent_set.create(price=rent)

        rent_estimate = _convert_price(
            row.get('rentzestimate_amount'),
        )
        rent_date = _get_date(row.get('rentzestimate_last_updated'))
        if rent_estimate and rent_date:
            if not listing.rentestimate_set.filter(
                estimate_date=rent_date
            ):
                rent_estimate = listing.rentestimate_set.create(
                    estimate_amount=rent_estimate
                )
                rent_estimate.estimate_date = rent_date

        sale_price = _convert_price(row.get('last_sold_price'))
        sale_date = _get_date(row.get('last_sold_date'))
        if sale_price and sale_date:
            if not listing.sale_set.filter(date=sale_date):
                sale = listing.sale_set.create(price=sale_price, date=sale_date)
                sale.date = sale_date

        estimate_amount = _convert_price(row.get('zestimate_amount'))
        estimate_date = _get_date(row.get('zestimate_last_updated'))
        if estimate_amount and estimate_date:
            if not listing.estimate_set.filter(estimate_date=estimate_date):
                estimate = listing.estimate_set.create(
                    estimate_amount=estimate_amount
                )
                estimate.estimate_date = estimate_date
