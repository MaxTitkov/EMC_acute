# Generated by Django 2.2.6 on 2019-10-25 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0002_info_current_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='patient',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='patient_info.Patient'),
        ),
    ]
