# Generated by Django 4.1.5 on 2024-10-10 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0003_position_zone_alter_position_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='position',
            name='requirements_is_html',
        ),
    ]
