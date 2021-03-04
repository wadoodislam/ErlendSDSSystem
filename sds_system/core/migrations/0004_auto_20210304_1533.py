# Generated by Django 3.1.1 on 2021-03-04 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210226_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name': 'SDS Producer'},
        ),
        migrations.AddField(
            model_name='sds_pdf',
            name='manual',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='revision_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='alias',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.manufacturer'),
        ),
        migrations.AlterField(
            model_name='sds_pdf',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.manufacturer'),
        ),
        migrations.AlterField(
            model_name='sds_pdf',
            name='pdf_md5',
            field=models.CharField(editable=False, max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sds_pdf',
            name='sds_download_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='sds_pdf',
            name='sds_product_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='SDSURLImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_to_pdf', models.URLField()),
                ('domain', models.CharField(max_length=100)),
                ('is_processed', models.BooleanField(null=True)),
                ('language', models.CharField(max_length=100)),
                ('sds_pdf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.sds_pdf')),
            ],
        ),
    ]