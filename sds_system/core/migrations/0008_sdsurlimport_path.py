# Generated by Django 3.1.1 on 2021-03-06 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210306_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdsurlimport',
            name='path',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
