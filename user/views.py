import json
import jwt
import requests

from vibe.settings import SECRET_KEY
from .models       import User
from music.models  import Album, Artist, ArtistAlbum
from .utils        import login_required

from datetime     import datetime
from django.views import View
from django.http  import HttpResponse, JsonResponse

class NaverSignInView(View):
    def get(self, request):
        naver_token = request.headers.get('Authorization', None)

        header = {'Authorization' : f"Bearer {naver_token}"}
        url = "https://openapi.naver.com/v1/nid/me"

        try:
            response = requests.get(url, headers = header, timeout = 2)
            user_data = response.json()['response']

            if User.objects.filter(naver_id = user_data.get('id')).exists():
                user = User.objects.get(naver_id = user_data.get('id'))
                token = jwt.encode({"user_id": user.naver_id}, SECRET_KEY['secret'], algorithm = 'HS256').decode('utf-8')

                return JsonResponse({"token": token,
                                     "user" : {"nickname": user.nickname, "image": user.image}}, status = 200)

            else:
                User(
                    naver_id    = user_data.get('id'),
                    nickname    = user_data.get('nickname'),
                    name        = user_data.get('name'),
                    email       = user_data.get('email'),
                    image       = user_data.get('profile_image'),
                    birthday    = datetime.strptime(user_data.get('birthday'), "%m-%d").date(),
                    gender      = user_data.get('gender'),
                ).save()

                user = User.objects.get(naver_id = user_data['id'])
                token = jwt.encode({"user_id": user.naver_id}, SECRET_KEY['secret'], algorithm = 'HS256').decode('utf-8')

                return JsonResponse({"token": token,
                                     "user" : {"nickname": user.nickname, "image": user.image}}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class LikeAlbumView(View):
    @login_required
    def get(self, request):
        limit = request.GET.get('limit', 10)
        like_albums = (
            Album
            .objects
            .all()
            .order_by('-like_count')[:limit]
        )

        like_album_list = [{
            'album_id'             : album.id,
            'album_name'           : album.name,
            'album_image'          : album.image,
            'album_artist_name'    : list(album.artistalbum_set.values_list('artist__name', flat = True))
        } for album in like_albums ]
        return JsonResponse({"like_album_list": like_album_list}, status = 200)
