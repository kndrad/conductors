# Generated by Django 3.2.9 on 2021-11-25 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alina', '0003_auto_20211125_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='timetable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alina.allocationtimetable', verbose_name='Plan służb'),
        ),
        migrations.AlterField(
            model_name='allocationdetail',
            name='allocation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alina.allocation', verbose_name='Służba'),
        ),
        migrations.AlterField(
            model_name='allocationtimetable',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
    ]
