import json

from .models      import User
from music.models import Theme

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
        self.assertEqual(response.json(),
            {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzNDU2NzgifQ.qsllxE7wljfDv0QjgmsuOU5vWnIe_g9W7bgYyGngg_M",
                "user" : {"nickname": "test_nickname", "image": "test_image"}
            }
        )
