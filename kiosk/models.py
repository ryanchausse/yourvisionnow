from django.db import models


class LensType(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Type'
        verbose_name_plural = 'Lens Types'


class LensMaterial(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Material'
        verbose_name_plural = 'Lens Materials'


class LensAddOns(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Add-On'
        verbose_name_plural = 'Lens Add-Ons'


class LensPackage(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    lens_type = models.ForeignKey(LensType, on_delete=models.CASCADE)
    lens_material = models.ForeignKey(LensMaterial, on_delete=models.CASCADE)
    lens_add_on = models.ForeignKey(LensAddOns, on_delete=models.CASCADE)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Package'
        verbose_name_plural = 'Lens Packages'


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class CustomerLensPackage(models.Model):
    order_name = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lens_package = models.ForeignKey(LensPackage, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_name

    class Meta:
        verbose_name = 'Customer and their Lens Package'
        verbose_name_plural = 'Customers and their Lens Packages'
