from django.db import models
from django.core.validators import ValidationError
from django.db.models import Q


class LensType(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Type'
        verbose_name_plural = 'Lens Types'


class MagnificationLevel(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Magnification Level'
        verbose_name_plural = 'Magnification Levels'


class LensMaterial(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Material'
        verbose_name_plural = 'Lens Materials'


class LensAddOns(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Add-On'
        verbose_name_plural = 'Lens Add-Ons'


class LensDesign(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Design'
        verbose_name_plural = 'Lens Designs'


class LensDesignItem(models.Model):
    # Relational table
    lens_design = models.ForeignKey(LensDesign, on_delete=models.CASCADE)
    lens_type = models.ForeignKey(LensType, on_delete=models.CASCADE, null=True, blank=True)
    lens_material = models.ForeignKey(LensMaterial, on_delete=models.CASCADE, null=True, blank=True)
    lens_add_on = models.ForeignKey(LensAddOns, on_delete=models.CASCADE, null=True, blank=True)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_type_retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_type_promo_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_material_retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_material_promo_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_add_on_retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lens_add_on_promo_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.lens_design} / { self.lens_type} / { self.lens_material} / { self.lens_add_on }'

    class Meta:
        verbose_name = 'Lens Designs and their items'
        verbose_name_plural = 'Lens Designs and their items'


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Order(models.Model):
    name = models.CharField(max_length=60)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    lens_design_item = models.ForeignKey(LensDesignItem, null=True, default=None, on_delete=models.CASCADE)
    notes = models.CharField(max_length=2000, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
