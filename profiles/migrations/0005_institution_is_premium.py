# Generated by Django 4.1.5 on 2024-11-26 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_voluntier_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='is_premium',
            field=models.BooleanField(default=False, verbose_name='Premium'),
        ),
    ]
