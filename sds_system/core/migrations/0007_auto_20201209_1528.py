# Generated by Django 3.1.1 on 2020-12-09 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201209_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sds_pdf_print_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sds_pdf_revision_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
