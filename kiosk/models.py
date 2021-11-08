from django.db import models


class LensType(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField()
    default_price = models.DecimalField()


class LensMaterial(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField()
    default_price = models.DecimalField()


class LensAddOns(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField()
    default_price = models.DecimalField()


class LensPackage(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField()
    lens_type = models.IntegerField(null=False)
    lens_material = models.IntegerField(null=False)
    lens_add_on = models.IntegerField(null=False)
    promo_price = models.DecimalField()
    retail_price = models.DecimalField()
