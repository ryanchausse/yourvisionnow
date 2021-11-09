from django.db import models


class LensType(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Lens Type'
        verbose_name_plural = 'Lens Types'


class LensMaterial(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Lens Material'
        verbose_name_plural = 'Lens Materials'


class LensAddOns(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Lens Add-On'
        verbose_name_plural = 'Lens Add-Ons'


class LensPackage(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    lens_type = models.IntegerField(null=False)
    lens_material = models.IntegerField(null=False)
    lens_add_on = models.IntegerField(null=False)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Lens Package'
        verbose_name_plural = 'Lens Packages'


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class CustomerLensPackage(models.Model):
    customer = models.IntegerField(null=False)
    lens_package = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'Customer and their Lens Package'
        verbose_name_plural = 'Customers and their Lens Packages'
