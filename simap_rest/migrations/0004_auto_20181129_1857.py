# Generated by Django 2.1.2 on 2018-11-29 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simap_rest', '0003_auto_20181129_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lan',
            old_name='HardwareField',
            new_name='hardwareField',
        ),
        migrations.RenameField(
            model_name='wan',
            old_name='HardwareField',
            new_name='hardwareField',
        ),
    ]
