# Generated by Django 3.0.3 on 2020-06-30 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20200630_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]