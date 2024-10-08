# Generated by Django 4.0 on 2024-09-10 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='positions.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='position',
            name='subcategory',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='positions.subcategory', verbose_name='Subcategory'),
        ),
    ]
