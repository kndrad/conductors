# Generated by Django 4.0 on 2022-01-19 19:01

import common.fields
import django.core.validators
from django.db import migrations
import re


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0010_waypoint_trail_waypoints_cant_repeat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trail',
            name='end',
            field=common.fields.LowerCaseCharField(max_length=128, validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9äöüÄÖÜaąćęłńóśźż ]*$'), code='invalid', message='Wpisz poprawną nazwę - nazwa nie może zawierać specjalnych znaków')], verbose_name='Koniec'),
        ),
        migrations.AlterField(
            model_name='trail',
            name='start',
            field=common.fields.LowerCaseCharField(max_length=128, validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9äöüÄÖÜaąćęłńóśźż ]*$'), code='invalid', message='Wpisz poprawną nazwę - nazwa nie może zawierać specjalnych znaków')], verbose_name='Początek'),
        ),
    ]
