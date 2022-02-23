# Generated by Django 3.2.8 on 2022-01-28 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0026_magnificationlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='lensdesignitem',
            name='lens_design_promo_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='lensdesignitem',
            name='lens_design_retail_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]