# Generated by Django 3.2.8 on 2021-11-09 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0002_auto_20211109_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerlenspackage',
            name='order_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
