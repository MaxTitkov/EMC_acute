# Generated by Django 2.2.6 on 2019-10-26 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0007_auto_20191026_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='fullname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
