# Generated by Django 3.0.5 on 2021-03-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Referal', '0026_auto_20210311_0953'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='occupied_fbeds',
            new_name='free_beds',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='occupied_mbeds',
            new_name='no_beds',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='tot_fbeds',
            new_name='occ_beds',
        ),
        migrations.RemoveField(
            model_name='room',
            name='room_desc',
        ),
        migrations.RemoveField(
            model_name='room',
            name='tot_mbeds',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='ward_desc',
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Both', 'Both')], max_length=50, null=True),
        ),
    ]