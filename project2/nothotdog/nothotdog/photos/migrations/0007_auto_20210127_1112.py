# Generated by Django 3.1.5 on 2021-01-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_auto_20210127_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
    ]
