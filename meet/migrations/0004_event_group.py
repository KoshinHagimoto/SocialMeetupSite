# Generated by Django 4.1.7 on 2023-04-12 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0003_alter_group_member_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meet.group'),
            preserve_default=False,
        ),
    ]
