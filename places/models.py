from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)

    description_short = models.TextField('Описание', blank=True, default='')
    description_long = models.TextField('Описание (html)', blank=True, default='')

    latitude = models.FloatField('Координата широты')
    longitude = models.FloatField('Координата долготы')

    def __str__(self):
        return self.title
