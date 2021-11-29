# Generated by Django 3.2.8 on 2021-11-29 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0014_auto_20211129_1554'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='lenspackageitem',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('lens_type__isnull', True), ('lens_material__isnull', False), ('lens_add_on__isnull', False)), models.Q(('lens_type__isnull', False), ('lens_material__isnull', True), ('lens_add_on__isnull', False)), models.Q(('lens_type__isnull', False), ('lens_material__isnull', False), ('lens_add_on__isnull', True)), _connector='OR'), name='only_one_of_three_lens_categories_allowed'),
        ),
    ]
