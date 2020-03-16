import json

from .models      import (
    Station,
    Theme,
    Music,
    Magazine,
    MusicMagazine,
    News,
    Recommendation,
    Album,
    ArtistAlbum,
    Artist
)

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

class MagazineView(View):
    def get(self, request):
        magazines = (
            Magazine
            .objects
            .all()
        )
        magazine_list = [{
            'magazine_id'       : magazine.id,
            'badge'             : magazine.badge,
            'release_date'      : magazine.release_date,
            'title'             : magazine.title,
            'description'       : magazine.description,
        } for magazine in magazines ]
        return JsonResponse({"magazine_list": magazine_list}, status = 200)
        
class MusicMagazineView(View):
    def get(self, request, magazine_id):
        try:
            music_magazine_list = (
                MusicMagazine
                .objects
                .filter(magazine_id = magazine_id)
                .select_related('music')
                .all()
            )
            music_magazine = [{
                'magazine_id'       : music_magazine.magazine_id,
                'music_name'        : music_magazine.music.name,                
                'music_album'       : music_magazine.music.album.name
            } for music_magazine in music_magazine_list ]
            return JsonResponse({"music_magazine": music_magazine}, status = 200)
        except Magazine.DoesNotExist:
            return JsonResponse({"message": "INVALID_MAGAZINE_ID"}, status = 400)

class NewsView(View):
    def get(self, request):
        news_all = (
            News
            .objects
            .all()
        )

        news_list = [{
            'news_id'        : news.id,
            'thumbnail'      : news.thumbnail,
            'main_text'      : news.main_text,
            'news_link'      : news.news_link
        } for news in news_all ]
        return JsonResponse({"news_list": news_list}, status = 200)
            
class RecommendationView(View):
    def get(self, request):        
        recommendations = (
            Recommendation
            .objects
            .all()
        )

        recommendation_list = [{
            'recommendation_id' : recommendation.id,
            'title'             : recommendation.title,
            'sub_title'         : recommendation.sub_title,
            'main_image'        : recommendation.main_image,
            'description'       : recommendation.description
        } for recommendation in recommendations ]
        return JsonResponse({"recommendation_list": recommendation_list}, status = 200)

class LatestAlbumView(View):
    def get(self, request):        
        latest_albums = (
            Album
            .objects
            .all()
            .order_by('-release_date')
        )            

        latest_album_list = [{
            'album_id'             : album.id,
            'album_name'           : album.name,
            'album_image'          : album.image,
            'album_artist_name'    : list(album.artistalbum_set.values_list('artist__name', flat = True))
        } for album in latest_albums ]
        return JsonResponse({"latest_album_list": latest_album_list}, status = 200)
