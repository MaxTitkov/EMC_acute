# Generated by Django 2.2.6 on 2019-10-25 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0003_auto_20191025_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_info.Patient'),
        ),
    ]
