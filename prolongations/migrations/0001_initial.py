# Generated by Django 4.0 on 2022-01-12 09:16

from django.db import migrations, models
import django.utils.timezone
import icals


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prolongation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(choices=[('FINE', 'Wezwania do zapłaty'), ('BLANKET', 'Bilety blankietowe'), ('REPLACEMENT', 'Bilety zastępcze')], default='FINE', max_length=128, verbose_name='Bilety')),
                ('last_renewal_date', models.DateField(default=django.utils.timezone.now, verbose_name='Data ostatniego przedłużenia')),
                ('expiration_date', models.DateField(blank=True, editable=False, null=True, verbose_name='Data wygaśnięcia')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'Prolongata',
                'verbose_name_plural': 'Prolongaty',
            },
            bases=(models.Model, icals.ICalConvertable),
        ),
        migrations.AddConstraint(
            model_name='prolongation',
            constraint=models.UniqueConstraint(fields=('user_id', 'ticket'), name='unique_user_prolongation'),
        ),
    ]
