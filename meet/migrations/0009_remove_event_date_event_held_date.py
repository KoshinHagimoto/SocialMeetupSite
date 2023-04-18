# Generated by Django 4.1.7 on 2023-04-14 04:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0008_alter_event_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='held_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 14, 4, 56, 25, 697942, tzinfo=datetime.timezone.utc), verbose_name='Date'),
            preserve_default=False,
        ),
    ]
