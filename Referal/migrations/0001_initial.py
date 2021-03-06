# Generated by Django 3.1.3 on 2020-12-27 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_type', models.CharField(choices=[('REFERAL HOSPIATAL', 'REFERAL HOSPITAL'), ('GENERAL HOSPITAL', 'GENERAL HOSPITAL'), ('PRIMARY HOSPITAL', 'PRIMARY HOSPITAL'), ('HEALTH CENTER', 'HEALTH CENTER')], max_length=30)),
                ('facility_name', models.CharField(max_length=25)),
                ('region', models.CharField(choices=[('ADDIS ABBABA', 'ADDIS ABBABA'), ('OROMIA', 'OROMIA'), ('AMHARA', 'AMHARA'), ('TIGRAY', 'TIGRAY'), ('SOUTH', 'SOUTH'), ('GAMBELLA', 'GAMBELLA'), ('BENSHANGUL', 'BENSHANGUL'), ('HARRARI', 'HARRARI'), ('DIREDAWA', 'DIREDAWA'), ('SIDAMA', 'SIDAMA'), ('SOUTH WEST', 'SOUTH WEST')], max_length=50)),
                ('subcity', models.CharField(max_length=25)),
                ('woreda', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Liaizon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('facility', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Referal.facility')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='RegionalAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('ADDIS ABBABA', 'ADDIS ABBABA'), ('OROMIA', 'OROMIA'), ('AMHARA', 'AMHARA'), ('TIGRAY', 'TIGRAY'), ('SOUTH', 'SOUTH'), ('GAMBELLA', 'GAMBELLA'), ('BENSHANGUL', 'BENSHANGUL'), ('HARRARI', 'HARRARI'), ('DIREDAWA', 'DIREDAWA'), ('SIDAMA', 'SIDAMA'), ('SOUTH WEST', 'SOUTH WEST')], max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReferTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer_to', models.PositiveIntegerField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referal.facility')),
            ],
        ),
        migrations.CreateModel(
            name='referalrequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_referal', models.CharField(choices=[('COLD', 'COLD'), ('EMERGENCY', 'EMERGENCY')], max_length=30)),
                ('name_of_patient', models.CharField(max_length=50)),
                ('paient_age', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10)),
                ('patient_region', models.CharField(choices=[('ADDIS ABBABA', 'ADDIS ABBABA'), ('OROMIA', 'OROMIA'), ('AMHARA', 'AMHARA'), ('TIGRAY', 'TIGRAY'), ('SOUTH', 'SOUTH'), ('GAMBELLA', 'GAMBELLA'), ('BENSHANGUL', 'BENSHANGUL'), ('HARRARI', 'HARRARI'), ('DIREDAWA', 'DIREDAWA'), ('SIDAMA', 'SIDAMA'), ('SOUTH WEST', 'SOUTH WEST')], max_length=35)),
                ('patient_subcity', models.CharField(max_length=25)),
                ('patient_woreda', models.CharField(max_length=25)),
                ('patient_phone', models.CharField(max_length=25)),
                ('chief_compliants', models.CharField(max_length=30)),
                ('diagnosis', models.CharField(max_length=30)),
                ('reason_for_referal', models.CharField(max_length=40)),
                ('refering_dr', models.CharField(max_length=25)),
                ('dr_phone', models.CharField(max_length=30)),
                ('blood_type', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('O', 'O'), ('A+', 'A+'), ('A-', 'A-'), ('AB-', 'AB-'), ('AB+', 'AB+'), ('O-', 'O-')], max_length=40)),
                ('blood_transfusion', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=40, null=True)),
                ('ambulance_driver_name', models.CharField(max_length=25)),
                ('ambulance_driver_phone', models.CharField(max_length=20)),
                ('ahp_name', models.CharField(max_length=25)),
                ('ahp_phone', models.CharField(max_length=25)),
                ('refered_date', models.DateTimeField(auto_now_add=True)),
                ('patient_diagnosis', models.CharField(blank=True, choices=[('THE SAME TO REFERING FACILITY', 'THE SAME TO REFERAL FACILLITY'), ('NOT THE SAME TO REFERING FACILITY', 'NOT THE SAME TO REFERING FACILITY')], max_length=40, null=True)),
                ('comments_of_referal', models.TextField(blank=True, max_length=250, null=True)),
                ('with_respect_to_medical_care', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=5, null=True)),
                ('with_respect_patient_transportation', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=5, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Feedback', 'Feedbak'), ('Re-direct', 'Re-direct')], default='Pending', max_length=50, null=True)),
                ('approved_date', models.DateTimeField(blank=True, null=True)),
                ('feedback_date', models.DateTimeField(blank=True, null=True)),
                ('re_referal_date', models.DateTimeField(blank=True, null=True)),
                ('reason_for_rereferal', models.CharField(blank=True, max_length=200, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to='Referal.liaizon')),
                ('feedback_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback_by', to='Referal.liaizon')),
                ('liaizon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='refered_by', to='Referal.liaizon')),
                ('re_referal_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='re_referal_by', to='Referal.liaizon')),
                ('referal_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referal.facility')),
                ('required_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referal.service')),
            ],
        ),
        migrations.CreateModel(
            name='CEO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('facility', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Referal.facility')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
