# Generated by Django 3.0.5 on 2021-03-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Referal', '0024_appoint_app_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appoint',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Waiting', 'Waiting'), ('Admitted', 'Admitted'), ('Not Available', 'Not Available'), ('Re-Appointed', 'Re-Appointed')], default='Waiting', max_length=50, null=True),
        ),
    ]
