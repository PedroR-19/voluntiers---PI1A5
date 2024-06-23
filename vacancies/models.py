from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=65)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    SHIFT_CHOICES = [
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ]
    
    COUNTRY_CHOICES = [
        ('BR', _('Brazil')),
        ('US', _('United States')),
    ]

    STATE_CHOICES = [
        ('SP', _('São Paulo')),
        ('RJ', _('Rio de Janeiro')),
    ]

    CITY_CHOICES = [
        ('São Paulo', _('São Paulo')),
        ('Rio de Janeiro', _('Rio de Janeiro')),
    ]

    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    requirements = models.TextField(verbose_name=_('Requirements'))
    requirements_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated_at'))
    cover = models.ImageField(
        upload_to='vacancies/covers/%Y/%m/%d/', blank=True, default='', verbose_name=_('Cover'))
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    profile = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('Profile')
    )
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default='morning', verbose_name=_('Shift'))
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, verbose_name=_('Country'))
    state = models.CharField(max_length=100, choices=STATE_CHOICES, verbose_name=_('State'))
    city = models.CharField(max_length=100, choices=CITY_CHOICES, verbose_name=_('City'))
    logradouro = models.CharField(max_length=255, verbose_name=_('Address'))
    days = models.ManyToManyField(Day, related_name='vacancies', verbose_name=_('Days'))  # Usando ManyToManyField para Dias

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancies:vacancy', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

class Application(models.Model):
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='applications_vaga', verbose_name=_('Vacancy'))
    voluntier = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/%Y/%m/%d/')
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

    def __str__(self):
        return f'{self.voluntier.username} - {self.vacancy.title}'

    class Meta:
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')
