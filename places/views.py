from django.shortcuts import render

from .models import Place


def show_index(request):
    places = Place.objects.all()

    return render(request, 'index.html', context={'places': places})
