# Generated by Django 3.2.9 on 2021-11-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('alina', '0007_auto_20211125_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traincrew',
            name='date',
            field=models.CharField(max_length=32, verbose_name='Data'),
        ),
    ]
