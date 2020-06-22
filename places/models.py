from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)

    description_short = models.TextField('Описание', blank=True, default='')
    description_long = models.TextField('Описание (html)', blank=True, default='')

    latitude = models.FloatField('Координата широты')
    longitude = models.FloatField('Координата долготы')

    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField('Название', max_length=200, blank=True, default='')
    image = models.ImageField('Изображение', upload_to='images')

    place = models.ForeignKey(Place,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              verbose_name='Место',
                              related_name='images'
                              )

    position = models.PositiveSmallIntegerField('Позиция', default=1)

    class Meta(object):
        ordering = ['position']

    def __str__(self):
        return self.name
