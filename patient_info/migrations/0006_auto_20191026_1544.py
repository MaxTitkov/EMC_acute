# Generated by Django 2.2.6 on 2019-10-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0005_patient_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='hided',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='fullname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
