# Generated by Django 3.2.9 on 2021-12-04 11:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('railroads', '0008_auto_20211203_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='arrival_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 11, 12, 46, 460971, tzinfo=utc), verbose_name='Czas przyjazdu'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='arrival_platform',
            field=models.CharField(default='NOTHING', max_length=32, verbose_name='Przyjazd na peron'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='arrival_station',
            field=models.CharField(default='NOTHING', max_length=64, verbose_name='Przyjazd na stację'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='departure_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 11, 13, 12, 320071, tzinfo=utc), verbose_name='Czas odjazdu'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='departure_platform',
            field=models.CharField(default='NOTHING', max_length=32, verbose_name='Odjazd z peronu'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='departure_station',
            field=models.CharField(default='NOTHING', max_length=64, verbose_name='Odjazd ze stacji'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicrailroadtrain',
            name='number',
            field=models.CharField(default='NOTHING', max_length=64, verbose_name='Numer'),
            preserve_default=False,
        ),
    ]
