# Generated by Django 3.0.7 on 2020-10-28 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20201027_2253'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set(),
        ),
    ]