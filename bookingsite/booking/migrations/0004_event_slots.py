# Generated by Django 3.0.3 on 2020-06-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20200630_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slots',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
