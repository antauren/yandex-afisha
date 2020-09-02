from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200)

    short_description = models.TextField('Описание', blank=True)
    long_description = HTMLField('Описание (html)', blank=True)

    latitude = models.FloatField('Координата широты')
    longitude = models.FloatField('Координата долготы')

    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField('Название', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='images')

    place = models.ForeignKey(Place,
                              on_delete=models.CASCADE,
                              verbose_name='Место',
                              related_name='images'
                              )

    position = models.PositiveSmallIntegerField('Позиция', default=1, db_index=True)

    class Meta(object):
        ordering = ('position',)

    def __str__(self):
        return self.name
