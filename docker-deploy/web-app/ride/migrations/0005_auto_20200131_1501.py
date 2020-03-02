# Generated by Django 3.0.2 on 2020-01-31 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ride', '0004_auto_20200129_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='rideowner',
            name='share_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='rideowner',
            name='share_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Ridesharer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=100)),
                ('earliest_arrive_date', models.DateTimeField(help_text='Format: 2020-01-01 12:00')),
                ('latest_arrive_date', models.DateTimeField(help_text='Format: 2020-01-01 13:00')),
                ('passenger_num', models.PositiveIntegerField()),
                ('sharer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
