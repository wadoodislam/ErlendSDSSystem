# Generated by Django 3.1.1 on 2021-03-06 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_sdsurlimport_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdsurlimport',
            name='download_failed',
            field=models.BooleanField(default=False),
        ),
    ]
