import json
import jwt
import requests

from .models      import User
from music.models import Theme
from vibe.settings import SECRET_KEY
from .models       import User
from music.models  import Album, Artist, ArtistAlbum

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

class NaverSignInTest(TestCase):
    client = Client()
    def setUp(self):
        Theme.objects.create(
            id   = 1,
            name = "기본테마"
        )

    def tearDown(self):
        Theme.objects.all().delete()

    @patch('user.views.requests')
    def test_user_signin_success(self, mocked_request):
        class NaverResponse:
            def json(self):
                return {
                    "resultcode": "00",
                    "message": "success",
                    "response": {
                        "email": "test@email.com",
                        "nickname": "test_nickname",
                        "profile_image": "test_image",
                        "age": "20-29",
                        "gender": "F",
                        "id": "12345678",
                        "name": "test_name",
                        "birthday": "10-11"
                    }
                }
        mocked_request.get = MagicMock(return_value = NaverResponse())

        client = Client()
        header = {'HTTP_Authorization': 'naver_token'}
        response = client.get('/user/naver_auth', content_type = 'applications/json', **header)

        self.assertEqual(response.status_code, 200)

    def test_user_signin_post_fail(self):
        client   = Client()
        header   = {'No_Authorizaeion' : '1234'}
        response = client.post('/user/naver_auth', content_type='application/json', **header)

        self.assertEqual(response.status_code, 405)

class LikeAlbumTest(TestCase):
    def setUp(self):
        client = Client()
        Album.objects.create(
            id                      = 1,
            name                    = "Lovely Sweet Heart",
            image                   = "https://musicmeta-phinf.pstatic.net/album/000/060/60001.jpg?type=r480Fll&v=20191212192801",
            like_count              = 2 
        )

        Album.objects.create(
            id                      = 2,
            name                    = "전설",
            image                   = "https://musicmeta-phinf.pstatic.net/album/002/923/2923941.jpg?type=r480Fll&v=20200218131711",
            like_count              = 1
        )

        Artist.objects.create(
            id                      = 1,
            name                    = "씨야(SeeYa)"
        )

        Artist.objects.create(
            id                      = 2,
            name                    = "잔나비"
        )

        ArtistAlbum.objects.create(
            artist                  = Artist.objects.get(id = 1),
            album                   = Album.objects.get(id = 1)
        )

        ArtistAlbum.objects.create(
            artist                  = Artist.objects.get(id = 2),
            album                   = Album.objects.get(id = 2)
        )

        Theme.objects.create(
            id                      = 1,
            name                    = "Theme1"
        )

        User.objects.create(
            naver_id    =  1,
            nickname    = "nickname",
            name        = "name",
            email       = "mail@mail.com",
            image       = "image",
            gender      = "M"
        )

    def tearDown(self):
        Artist.objects.all().delete()
        Album.objects.all().delete()
        ArtistAlbum.objects.all().delete()
        User.objects.all().delete()

    def test_likealbum_get_success(self):
        client = Client()
        token = jwt.encode({"user_id": 1}, SECRET_KEY['secret'], algorithm = 'HS256').decode('utf-8')
        header = {'HTTP_Authorization': token}
        response = client.get('/user/album', **header, content_type = 'applications/json')
        self.assertEqual(response.json(),
            {
                "like_album_list" : [
                    {
                        'album_id'              :  1,
                        'album_name'            :  "Lovely Sweet Heart",
                        'album_image'           :  "https://musicmeta-phinf.pstatic.net/album/000/060/60001.jpg?type=r480Fll&v=20191212192801",
                        'album_artist_name'     :  ["씨야(SeeYa)"]
                    },
                    {
                        'album_id'              : 2,
                        'album_name'            : "전설",
                        'album_image'           : "https://musicmeta-phinf.pstatic.net/album/002/923/2923941.jpg?type=r480Fll&v=20200218131711",
                        'album_artist_name'     : ["잔나비"]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
