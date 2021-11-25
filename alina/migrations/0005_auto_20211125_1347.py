# Generated by Django 3.2.9 on 2021-11-25 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alina', '0004_auto_20211125_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocationdetail',
            name='action',
            field=models.CharField(max_length=128, null=True, verbose_name='Akcja'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='allocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alina.allocation', verbose_name='Służba'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='end_hour',
            field=models.CharField(max_length=32, null=True, verbose_name='Godzina'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='end_location',
            field=models.CharField(max_length=128, null=True, verbose_name='lokalizacja końcowa'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='start_hour',
            field=models.CharField(max_length=32, null=True, verbose_name='Godzina'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='start_location',
            field=models.CharField(max_length=128, null=True, verbose_name='Lokalizacja początkowa'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='train_number',
            field=models.CharField(max_length=32, null=True, verbose_name='Number pociągu'),
        ),
    ]
