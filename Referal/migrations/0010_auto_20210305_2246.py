# Generated by Django 3.0.5 on 2021-03-05 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Referal', '0009_auto_20210305_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='facility',
            new_name='facility_id',
        ),
    ]
