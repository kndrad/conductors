# Generated by Django 3.2.9 on 2021-11-30 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alina', '0010_alter_allocationtimetable_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='allocationtimetable',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='train_number',
            field=models.CharField(max_length=32, null=True, verbose_name='Numer pociągu'),
        ),
    ]
