import json

from .models import (
    Station,
    Theme,
    Music,
    Magazine,
    MusicMagazine,
    News,
    Recommendation,
    Album,
    ArtistAlbum,
    Artist,
    Video
)

from vibe.settings import MEDIA_URL
from user.models   import User
from user.utils    import check_login

from django.views import View
from django.http  import HttpResponse, JsonResponse, StreamingHttpResponse

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

class UserThemeView(View):
    @check_login
    def get(self, request, theme_id):
        try:
            theme = Theme.objects.get(id = theme_id)
            if request.user:
                request.user.theme_id = theme_id
                request.user.save()
                return HttpResponse(status = 200)

            return HttpResponse(status = 200)

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
            'thumbnail'         : magazine.thumbnail,
            'badge'             : magazine.badge,
            'release_date'      : magazine.release_date,
            'title'             : magazine.title,
            'description'       : magazine.description,
        } for magazine in magazines ]
        return JsonResponse({"magazine_list": magazine_list}, status = 200)

class MusicMagazineView(View):
    def get(self, request, magazine_id):
        limit = request.GET.get('limit', 20)
        try:
            music_magazine_list = (
                MusicMagazine
                .objects
                .filter(magazine_id = magazine_id)
                .select_related('music')
                .all()[:limit]
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
        limit = request.GET.get('limit', 10)
        news_all = (
            News
            .objects
            .all()[:limit]
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
        limit = request.GET.get('limit', 17)
        recommendations = (
            Recommendation
            .objects
            .all()[:limit]
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
        limit = request.GET.get('limit', 15)        
        latest_albums = (
            Album
            .objects
            .all()
            .order_by('-release_date')[:limit]
        )

        latest_album_list = [{
            'album_id'             : album.id,
            'album_name'           : album.name,
            'album_image'          : album.image,
            'album_artist_name'    : list(album.artistalbum_set.values_list('artist__name', flat = True)) 
        } for album in latest_albums ]
        return JsonResponse({"latest_album_list": latest_album_list}, status = 200)

def get_music_list(musics):
    music_list = [
        {
            'music_id'     : music.id,
            'music_name'   : music.name,
            'track_number' : music.track_number,
            'album_image'  : music.album.image,
            'album_name'   : music.album.name,
            'album_id'     : music.album.id,
            'lyrics'       : music.lyrics,
            'artist_name'  : list(music.artistmusic_set.values_list('artist__name', flat = True)),
            'artist_id'    : list(music.artistmusic_set.values_list('artist__id', flat = True))
        } for music in musics]
    return music_list

class RecommendationMusicView(View):
    def get(self, request, recommendation_id):
        try:
            musics = Music.objects.filter(recommendationmusic__recommendation_id = recommendation_id)
            recommendation_details = list(musics
                                          .values(
                                              'recommendation__title',
                                              'recommendation__sub_title',
                                              'recommendation__main_image',
                                              'recommendation__description'))[0]

            return JsonResponse({"recommendation": recommendation_details,
                                 "music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class StationMusicView(View):
    def get(self, request, station_id):
        try:
            musics = Music.objects.filter(stationmusic__station_id = station_id)
            station_details = list(musics
                                   .values(
                                       'station__name',
                                       'station__description'))[0]

            return JsonResponse({"station": station_details,
                                 "music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class AlbumMusicView(View):
    def get(self, request, album_id):
        try:
            musics = Music.objects.filter(album_id = album_id).prefetch_related('artistmusic_set')
            album_details = list(musics
                                 .values(
                                     'album__name',
                                     'album__image',
                                     'album__release_date',
                                     'album__description',
                                     'album__genre__name',
                                     'artist__name'))[0]

            return JsonResponse({"album_details": album_details,
                                 "music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class ArtistMusicView(View):
    def get(self, request, artist_id):
        try:
            musics = Music.objects.filter(artistmusic__artist_id = artist_id)
            return JsonResponse({"music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class StationMusicView(View):
    def get(self, request, station_id):
        try:
            musics = Music.objects.filter(stationmusic__station_id = station_id)
            station_details = list(musics
                                   .values(
                                       'station__name',
                                       'station__description'))[0]

            return JsonResponse({"station": station_details,
                                 "music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class AlbumMusicView(View):
    def get(self, request, album_id):
        try:
            musics = Music.objects.filter(album_id = album_id).prefetch_related('artistmusic_set')
            album_details = list(musics
                                 .values(
                                     'album__name',
                                     'album__image',
                                     'album__release_date',
                                     'album__description',
                                     'album__genre__name',
                                     'artist__name'))[0]

            return JsonResponse({"album_details": album_details,
                                 "music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class ArtistMusicView(View):
    def get(self, request, artist_id):
        try:
            musics = Music.objects.filter(artistmusic__artist_id = artist_id)
            return JsonResponse({"music_list": get_music_list(musics)}, status = 200)

        except IndexError:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class AlbumListView(View):
    def get(self, request, artist_id):
        albums = Album.objects.prefetch_related('artistalbum_set').filter(artist__id = artist_id)
        album_details = [
            {
                'id'          : album.id,
                'name'        : album.name,
                'image'       : album.image,
                'artist_name' : list(album.artistalbum_set.values_list('artist__name', flat = True))
            } for album in albums]
        return JsonResponse({"album": album_details}, status = 200)

class MusicView(View):
    def get(self, request, music_id):
        try:
            music = Music.objects.prefetch_related('artistmusic_set').get(id = music_id)

            music_details = {
                'name'        : music.name,
                'writer'      : music.writer,
                'composer'    : music.composer,
                'arranger'    : music.arranger,
                'lyrics'      : music.lyrics,
                'artist_id'   : list(music.artistmusic_set.values_list('artist__id', flat = True)),
                'artist_name' : list(music.artistmusic_set.values_list('artist__name', flat = True))
            }

            return JsonResponse({"music": music_details}, status = 200)

        except Music.DoesNotExist:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class ArtistView(View):
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.prefetch_related('artistgenre_set').get(id = artist_id)

            artist_details = {
                'name'       : artist.name,
                'image'      : artist.image,
                'debut_date' : artist.debut_date,
                'genre'      : list(artist.artistgenre_set.values_list('genre__name', flat = True))
            }

            return JsonResponse({"artist": artist_details}, status = 200)

        except Artist.DoesNotExist:
                return JsonResponse({"message": "ARTIST_DOES_NOT_EXIST"}, status = 400)

class MusicPlayView(View):
    def get(self, request, music_id):
        try:
            music = Music.objects.prefetch_related('artistmusic_set').get(id = music_id)

            music_details = {
                'id'          : music.id,
                'name'        : music.name,
                'play_time'   : music.play_time.strftime("%M:%S"),
                'album_image' : music.album.image,
                'artist_name' : list(music.artistmusic_set.values_list('artist__name', flat = True)),
                'lyrics'      : music.lyrics
            }

            return JsonResponse({"music": music_details}, status = 200)

        except Music.DoesNotExist:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

class MusicStreamView(View):
    def get(self, request, music_id):
        try:
            music    = Music.objects.get(id = music_id)
            content  = MEDIA_URL + f"{music_id}.mp3"
            response = StreamingHttpResponse(self.iterator(content),
                                             status = 200,
                                             content_type = 'audio/mp3')

            response['Cache-Control'] = 'no-cache'
            response['Content-Disposition'] = f'filename = {music_id}.mp3'
            response['Content-Length'] = len(open(content,'rb').read())
            return response

        except Music.DoesNotExist:
            return JsonResponse({"message": "MUSIC_DOES_NOT_EXIST"}, status = 400)

        except FileNotFoundError:
            return JsonResponse({"message": "FILE_DOES_NOT_EXIST"}, status = 400)

    def iterator(self, content):
        with open(content, 'rb') as music:
            while True:
                read_music = music.read()
                if read_music:
                    yield read_music
                else:
                    break

class MusicSearchView(View):
    def get(self, request):        
        limit = request.GET.get('limit', 20)
        query = request.GET.get('query', None)

        if query is not None:
            musics     = Music.objects.filter(name__icontains = query)[:limit]
            music_list = [{
                "id"                  : music.id,
                "music_name"          : music.name,
                "album_image"         : music.album.image if music.album else None,
                "artist_name"         : list(music.artistmusic_set.values_list('artist__name', flat = True))
                } for music in musics]

            albums     = Album.objects.filter(name__icontains = query)[:limit]
            album_list = [{
                "id"                  : album.id,
                "album_name"          : album.name,
                "album_image"         : album.image,
                "artist_name"         : list(album.artistalbum_set.values_list('artist__name', flat = True))
            } for album in albums]

            videos     = Video.objects.filter(name__icontains = query)[:limit]
            video_list = [{
                "id"                  : video.id,
                "video_name"          : video.name,
                "video_image"         : video.main_image,
                "artist_name"         : list(video.artistvideo_set.values_list('artist__name', flat = True))
            } for video in videos]

            lyrics_list = Music.objects.filter(lyrics__icontains = query)[:limit]
            lyrics_list = [{
                "id"                 : lyrics.id,
                "lyrics"             : lyrics.lyrics,
                "music_name"         : lyrics.name,
                "lyrics_writer"      : lyrics.writer,
                "album_image"        : lyrics.album.image if lyrics.album else None
            } for lyrics in lyrics_list]
            
            return JsonResponse(
                {
                    "music_list"     : music_list,
                    "album_list"     : album_list,
                    "video_list"     : video_list,
                    "lyrics_list"    : lyrics_list
                }, status = 200)



        
