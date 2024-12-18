from django.contrib.auth.models import User
from django.conf                import settings
from django.db                  import models
from django.urls                import reverse
from django.utils.text          import slugify
from django.utils.translation   import gettext_lazy as _

from profiles.models import Institution, Voluntier


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name     = models.CharField(max_length=65)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Position(models.Model):
    SHIFT_CHOICES = [
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ]


    title        = models.CharField(max_length=65, verbose_name=_('Title'))
    description  = models.CharField(max_length=165, verbose_name=_('Description'))
    slug         = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated_at'))

    cover = models.ImageField(
        upload_to='positions/covers/%Y/%m/%d/', 
        blank=True, 
        default='', 
        verbose_name=_('Cover')
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        default=None, 
        verbose_name=_('Category')
    )

    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        default=None, 
        verbose_name=_('Subcategory')
    )

    profile = models.ForeignKey(Institution, on_delete=models.CASCADE)

    shift        = models.CharField(max_length=10, choices=SHIFT_CHOICES, default='morning', verbose_name=_('Shift'))
    cep          = models.CharField(max_length=100, verbose_name=_('cep'))
    state        = models.CharField(max_length=100, verbose_name=_('State'))
    city         = models.CharField(max_length=100, verbose_name=_('City'))
    neighborhood = models.CharField(max_length=100, verbose_name=_('Neighborhood'), default='')
    street       = models.CharField(max_length=255, verbose_name=_('Street'), default='')
    more         = models.CharField(max_length=255, verbose_name=_('More'), default='')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('positions:position', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)


class Application(models.Model):
    position  = models.ForeignKey('position', on_delete=models.CASCADE, related_name='applications_vaga', verbose_name=_('position'))
    voluntier = models.ForeignKey(Voluntier, on_delete=models.CASCADE)

    cv   = models.FileField(upload_to='cvs/%Y/%m/%d/')
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

    def __str__(self):
        return f'{self.voluntier.email} - {self.position.title}'

    class Meta:
        verbose_name        = _('position')
        verbose_name_plural = _('positions')