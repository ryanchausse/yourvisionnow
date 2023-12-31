# Generated by Django 3.2.8 on 2021-11-29 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0013_alter_lenspackageitem_lens_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lenspackageitem',
            name='lens_add_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kiosk.lensaddons'),
        ),
        migrations.AlterField(
            model_name='lenspackageitem',
            name='lens_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kiosk.lensmaterial'),
        ),
        migrations.AlterField(
            model_name='lenspackageitem',
            name='lens_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kiosk.lenstype'),
        ),
    ]
