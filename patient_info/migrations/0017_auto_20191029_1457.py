# Generated by Django 2.2.6 on 2019-10-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0016_info_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='drisk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='srisk',
            field=models.BooleanField(default=False),
        ),
    ]
