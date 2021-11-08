from django.db import models


class LensType(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)


class LensMaterial(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)


class LensAddOns(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)


class LensPackage(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    lens_type = models.IntegerField(null=False)
    lens_material = models.IntegerField(null=False)
    lens_add_on = models.IntegerField(null=False)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class CustomerLensPackage(models.Model):
    customer = models.IntegerField(null=False)
    lens_package = models.IntegerField(null=False)
