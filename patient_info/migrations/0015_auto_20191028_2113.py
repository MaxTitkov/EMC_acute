# Generated by Django 2.2.6 on 2019-10-28 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_info', '0014_remove_info_bathroom_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='bathroom_time',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='record',
            field=models.TextField(blank=True, null=True),
        ),
    ]