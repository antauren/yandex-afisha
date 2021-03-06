from django.shortcuts import render, get_object_or_404, reverse
from django.http import JsonResponse

from .models import Place


def show_index(request):
    places = {
        'type': 'FeatureCollection',
        'features': [{'type': 'Feature',
                      'geometry': {'type': 'Point',
                                   'coordinates': [place.longitude, place.latitude]
                                   },
                      'properties': {'title': place.title,
                                     'placeId': place.id,
                                     'detailsUrl': reverse('show_place', kwargs={'place_id': place.id})
                                     }
                      }
                     for place in Place.objects.all()]
    }

    return render(request, 'index.html', context={'places': places})


def show_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    response_dict = {
        'title': place.title,
        'imgs': [p_image.image.url for p_image in place.images.all()],
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude
        }
    }

    return JsonResponse(response_dict, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})
