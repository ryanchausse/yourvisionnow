from django.db import models
from django.core.validators import ValidationError
from django.db.models import Q


class LensType(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    default_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
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
    default_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
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
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Design'
        verbose_name_plural = 'Lens Designs'


class LensDesignItem(models.Model):
    # Relational table
    lens_type = models.ForeignKey(LensType, on_delete=models.CASCADE, null=True, blank=True)
    lens_design = models.ForeignKey(LensDesign, on_delete=models.CASCADE)
    lens_material = models.ForeignKey(LensMaterial, on_delete=models.CASCADE, null=True, blank=True)
    lens_add_on = models.ForeignKey(LensAddOns, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.lens_design} / { self.lens_type} / { self.lens_material} / { self.lens_add_on }'

    def clean(self):
        # Only a single lens_type, lens_material, or lens_add_on can be set for each lens_package (relational)
        if (self.lens_type and self.lens_material) \
                or (self.lens_type and self.lens_add_on) \
                or (self.lens_material and self.lens_add_on):
            raise ValidationError('Only one of lens_type, lens_material, or lens_add_on can be set. '
                                  'Please make separate records for the items in a lens package.')

    class Meta:
        verbose_name = 'Lens Designs and their items'
        verbose_name_plural = 'Lens Designs and their items'
        constraints = [
            models.CheckConstraint(
                check=(
                            Q(lens_type__isnull=False) &
                            Q(lens_material__isnull=True) &
                            Q(lens_add_on__isnull=True)
                      ) | (
                            Q(lens_type__isnull=True) &
                            Q(lens_material__isnull=False) &
                            Q(lens_add_on__isnull=True)
                      ) | (
                            Q(lens_type__isnull=True) &
                            Q(lens_material__isnull=True) &
                            Q(lens_add_on__isnull=False)
                ),
                name='lens_design_only_one_of_three_lens_categories_allowed'
            )
        ]


class LensPackage(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    promo_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    static_img_url = models.CharField(max_length=255, default='multiple_lenses.jpg')
    uploaded_img = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lens Package'
        verbose_name_plural = 'Lens Packages'


class LensPackageItem(models.Model):
    # Relational table
    lens_package = models.ForeignKey(LensPackage, on_delete=models.CASCADE)
    lens_type = models.ForeignKey(LensType, on_delete=models.CASCADE, null=True, blank=True)
    lens_material = models.ForeignKey(LensMaterial, on_delete=models.CASCADE, null=True, blank=True)
    lens_add_on = models.ForeignKey(LensAddOns, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.lens_package} / { self.lens_type} / { self.lens_material} / { self.lens_add_on }'

    def clean(self):
        # Only a single lens_type, lens_material, or lens_add_on can be set for each lens_package (relational)
        if (self.lens_type and self.lens_material) \
                or (self.lens_type and self.lens_add_on) \
                or (self.lens_material and self.lens_add_on):
            raise ValidationError('Only one of lens_type, lens_material, or lens_add_on can be set. '
                                  'Please make separate records for the items in a lens package.')

    class Meta:
        verbose_name = 'Lens Packages and their items'
        verbose_name_plural = 'Lens Packages and their items'
        constraints = [
            models.CheckConstraint(
                check=(
                            Q(lens_type__isnull=False) &
                            Q(lens_material__isnull=True) &
                            Q(lens_add_on__isnull=True)
                      ) | (
                            Q(lens_type__isnull=True) &
                            Q(lens_material__isnull=False) &
                            Q(lens_add_on__isnull=True)
                      ) | (
                            Q(lens_type__isnull=True) &
                            Q(lens_material__isnull=True) &
                            Q(lens_add_on__isnull=False)
                ),
                name='lens_package_only_one_of_three_lens_categories_allowed'
            )
        ]


class Stages:
    # To allow admins to change the order of top level items as presented to the customer
    lens_package = models.ForeignKey(LensPackage, on_delete=models.CASCADE, null=True)
    lens_type = models.ForeignKey(LensType, on_delete=models.CASCADE, null=True)
    lens_material = models.ForeignKey(LensMaterial, on_delete=models.CASCADE, null=True)
    lens_add_on = models.ForeignKey(LensAddOns, on_delete=models.CASCADE, null=True)
    order_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.lens_package} / { self.lens_type} / { self.lens_material} /' \
               f' { self.lens_add_on } / { self.order_position }'

    class Meta:
        verbose_name = 'Lens Packages and their items'
        verbose_name_plural = 'Lens Packages and their items'


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
    lens_package = models.ForeignKey(LensPackage, null=True, default=None, on_delete=models.CASCADE)
    notes = models.CharField(max_length=2000, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
