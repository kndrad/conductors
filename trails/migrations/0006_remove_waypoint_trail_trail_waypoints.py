# Generated by Django 4.0 on 2022-01-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0005_remove_trail_waypoints_waypoint_trail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waypoint',
            name='trail',
        ),
        migrations.AddField(
            model_name='trail',
            name='waypoints',
            field=models.ManyToManyField(related_name='waypoints', to='trails.Waypoint', verbose_name='Punkty na szlaku'),
        ),
    ]
