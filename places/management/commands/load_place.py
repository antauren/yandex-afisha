import json
import os

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from tqdm import tqdm
from urllib3.util import parse_url

from places.models import Image, Place


class Command(BaseCommand):
    help = 'Add places to the map.'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', action='store_true')
        parser.add_argument('-f', '--files',
                            required=False,
                            nargs='+',
                            type=str,
                            default=[]
                            )

    def handle(self, *args, **options):
        data_dir = os.path.join('places', 'data')

        place_filenames = os.listdir(data_dir) if options['all'] else options['files']

        for filename in tqdm(place_filenames, desc='json-files handling'):
            _, ext = os.path.splitext(filename)
            if ext.lower() != '.json':
                continue

            json_path = os.path.join(data_dir, filename)

            if not (os.path.exists(json_path) and os.path.isfile(json_path)):
                continue

            try:
                place_data = read_json(json_path)
            except (UnicodeDecodeError, json.decoder.JSONDecodeError) as err:
                tqdm.write('Filename: {}\nError: {}\n'.format(filename, err))
                continue

            try:
                create_place(place_data)
            except KeyError as err:
                tqdm.write('Filename: {}\nError: {}\n'.format(filename, err))


def create_place(place_data: dict):
    place, _ = Place.objects.update_or_create(latitude=place_data['coordinates']['lat'],
                                              longitude=place_data['coordinates']['lng'],

                                              defaults={
                                                  'title': place_data['title'],
                                                  'short_description': place_data['description_short'],
                                                  'long_description': place_data['description_long'],
                                              },
                                              )

    for num, img_url in enumerate(place_data['imgs']):
        try:
            response = requests.get(img_url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.MissingSchema):
            continue

        filename = get_filename_from_url(img_url)

        img_obj, _ = Image.objects.update_or_create(place=place,
                                                    name=filename,

                                                    defaults={
                                                        'position': num + 1,
                                                    },
                                                    )
        img_obj.image.save(filename, ContentFile(response.content))


def get_filename_from_url(url):
    parsed_url = parse_url(url)
    _, filename = os.path.split(parsed_url.path)

    return filename


def read_json(path, encoding='UTF-8'):
    with open(path, encoding=encoding) as fd:
        return json.load(fd)
