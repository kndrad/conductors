# Generated by Django 3.2.9 on 2021-11-30 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railroads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='railroadstation',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Nazwa stacji kolejowej'),
        ),
    ]
