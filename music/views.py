import json

from .models import Station, Theme

from django.views import View
from django.http  import HttpResponse, JsonResponse

class StationView(View):
    def get(self, request):
        return JsonResponse({"station_list": list(Station.objects.values())}, status = 200)

class ThemeView(View):
    def get(self, request):
        theme_list = Theme.objects.values('id', 'main_image', 'name', 'creator')
        return JsonResponse({"theme_list": list(theme_list)[:-1]}, status = 200)

class StationThemeView(View):
    def get(self, request, theme_id):
        try:
            theme = Theme.objects.prefetch_related('stationtheme_set').get(id = theme_id)

            theme_details = {
                'image'    : theme.main_image,
                'category' : theme.category,
                'name'     : theme.name,
                'creator'  : theme.creator,
                'charge'   : theme.charge
            }

            theme_images = list(theme.stationtheme_set.values('station_id', 'image'))

            return JsonResponse({"theme_details": theme_details,
                                 "theme_images" : theme_images}, status = 200)

        except Theme.DoesNotExist:
            return JsonResponse({"message": "THEME_DOES_NOT_EXIST"}, status = 400)
