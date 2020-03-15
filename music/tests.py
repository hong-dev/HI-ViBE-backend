import json

from .models import Station, Theme, StationTheme

from django.test import TestCase
from django.test import Client

class StationThemeTest(TestCase):
    def setUp(self):
        client = Client()
        Station.objects.create(
            id          = 1,
            name        = "힙터질때",
            description = "빌보드 200 차트에서도 1위를 차지하며 음악 역사를 새로 쓰고 있는 방탄소년단은 이제 힙의 다음 수준을 제시하고 있는 경지다. 늘 그랬듯이 한국어 가사로 만든 노래, 별다른 특수효과도 아무런 장치도 없이 그저 방탄소년단에게만 집중한 뮤직비디오까지 이것이 국가적 차원의 힙이다."
        )

        Theme.objects.create(
            id         = 1,
            category   = "VIBE 공식 테마",
            charge     = "무료",
            creator    = "바나나컬쳐",
            main_image = "https://music-phinf.pstatic.net/20181016_220/15396574205433iLX1_PNG/theme_main_cover_EXID.png?type=w720",
            name       = "EXID의 핫한 VIBE"
        )

        Theme.objects.create(
            id         = 2,
            category   = "VIBE 공식 테마",
            charge     = "무료",
            creator    = "P NATION",
            main_image = "https://music-phinf.pstatic.net/20191202_84/1575273368910ItDE8_PNG/theme_main_cover_%C5%A9%B7%AF%BD%AC.png?type=w720",
            name       = "Crush네 Vinyl봉지"
        )

        StationTheme.objects.create(
            station = Station.objects.get(id=1),
            theme   = Theme.objects.get(id=1),
            image   = "https://music-phinf.pstatic.net/20181016_162/1539657286188xCDN3_PNG/dj_1_mood_EXID_1.png?type=w720"
        )

    def tearDown(self):
        Station.objects.all().delete()
        Theme.objects.all().delete()
        StationTheme.objects.all().delete()

    def test_station_get_success(self):
        client = Client()
        response = client.get('/music/station')
        self.assertEqual(response.json(),
            {
                "station_list" : [
                    {
                        "id"          : 1,
                        "name"        : "힙터질때",
                        "description" : "빌보드 200 차트에서도 1위를 차지하며 음악 역사를 새로 쓰고 있는 방탄소년단은 이제 힙의 다음 수준을 제시하고 있는 경지다. 늘 그랬듯이 한국어 가사로 만든 노래, 별다른 특수효과도 아무런 장치도 없이 그저 방탄소년단에게만 집중한 뮤직비디오까지 이것이 국가적 차원의 힙이다."
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_theme_get_success(self):
        client = Client()
        response = client.get('/music/station/theme')
        self.assertEqual(response.json(),
            {
                "theme_list" : [
                    {
                        "id"         : 1,
                        "name"       : "EXID의 핫한 VIBE",
                        "main_image" : "https://music-phinf.pstatic.net/20181016_220/15396574205433iLX1_PNG/theme_main_cover_EXID.png?type=w720",
                        "creator"    : "바나나컬쳐"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_station_theme_get_success(self):
        client = Client()
        response = client.get('/music/station/theme1')
        self.assertEqual(response.json(),
            {
                "theme_details": {
                    "category" : "VIBE 공식 테마",
                    "charge"   : "무료",
                    "creator"  : "바나나컬쳐",
                    "image"    : "https://music-phinf.pstatic.net/20181016_220/15396574205433iLX1_PNG/theme_main_cover_EXID.png?type=w720",
                    "name"     : "EXID의 핫한 VIBE"
                },
                "theme_images": [
                    {
                        "image"      : "https://music-phinf.pstatic.net/20181016_162/1539657286188xCDN3_PNG/dj_1_mood_EXID_1.png?type=w720",
                        "station_id" : 1
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_station_theme_get_fail(self):
        client = Client()
        response = client.get('/music/station/theme100')
        self.assertEqual(response.json(),
            {
                'message' : 'THEME_DOES_NOT_EXIST'
            }
        )
        self.assertEqual(response.status_code, 400)
