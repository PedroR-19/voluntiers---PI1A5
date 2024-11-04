# Generated by Django 5.1.1 on 2024-11-03 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='cvs/%Y/%m/%d/')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65, verbose_name='Title')),
                ('description', models.CharField(max_length=165, verbose_name='Description')),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated_at')),
                ('cover', models.ImageField(blank=True, default='', upload_to='positions/covers/%Y/%m/%d/', verbose_name='Cover')),
                ('shift', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')], default='morning', max_length=10, verbose_name='Shift')),
                ('state', models.CharField(choices=[('SP', 'São Paulo'), ('RJ', 'Rio de Janeiro')], max_length=100, verbose_name='State')),
                ('city', models.CharField(choices=[('São Paulo', 'São Paulo'), ('Rio de Janeiro', 'Rio de Janeiro')], max_length=100, verbose_name='City')),
                ('zone', models.CharField(choices=[('Central', 'Central'), ('Leste', 'Leste'), ('Oeste', 'Oeste'), ('Norte', 'Norte'), ('Sul', 'Sul')], default='', max_length=100, verbose_name='Zone')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Address')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65)),
            ],
        ),
    ]
