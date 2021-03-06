# Generated by Django 3.0.5 on 2021-03-04 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Referal', '0005_remove_facility_user_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='occupied_bed',
            new_name='occupied_fbeds',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='tot_beds',
            new_name='occupied_mbeds',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='room',
            name='creator',
        ),
        migrations.AddField(
            model_name='room',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Referal.Facility_User'),
        ),
        migrations.AddField(
            model_name='room',
            name='tot_fbeds',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='tot_mbeds',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ward',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referal.Facility_User'),
        ),
    ]
