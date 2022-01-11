# Generated by Django 4.0 on 2022-01-11 21:38

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
import utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationAtTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', utils.fields.LowercaseCharField(max_length=128, verbose_name='Nazwa stacji')),
            ],
            options={
                'verbose_name': 'Stacja na szlaku',
                'verbose_name_plural': 'Stacje na szlaku',
            },
        ),
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning', models.CharField(max_length=128, verbose_name='Początek szlaku')),
                ('finale', models.CharField(max_length=128, verbose_name='Koniec szlaku')),
                ('last_driven', models.DateField(default=django.utils.timezone.now, verbose_name='Data ostatniego przejazdu')),
                ('stations', models.ManyToManyField(blank=True, to='trails.StationAtTrail', verbose_name='Stacje na szlaku')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'Szlak',
                'verbose_name_plural': 'Szlaki',
            },
        ),
        migrations.AddConstraint(
            model_name='trail',
            constraint=models.CheckConstraint(check=models.Q(('beginning', django.db.models.expressions.F('finale')), _negated=True), name='trail_beginning_and_finale_cannot_be_equal'),
        ),
    ]
