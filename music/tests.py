import json

from .models import (
    Station,
    Theme,
    StationTheme,
    Magazine,
    MusicMagazine,
    News,
    Recommendation,
    Album,
    ArtistAlbum,
    Artist
)

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

class MagazineTest(TestCase):
    def setUp(self):
        client = Client()
        Magazine.objects.create(    
            id                = 1,
            badge             = "https://music-phinf.pstatic.net/20190702_287/1562066500033t4gp0_PNG/icon_pick.png",
            release_date      = "2020-03-10",
            title             = "이주의 디깅 #49 \\n임영웅",
            description       = "지상파 이외 채널 프로그램으로는 가장 높은 시청률이라는 대기록을 세운 ‘내일은 미스터트롯’이 많은 사랑을 받고 있다. 갑자기 웬 트로트 붐이냐?라고 하는 사람들도 있겠지만 사실 트로트는 아주 오래전부터 우리와 함께해 왔다. 세대가 바뀌면서 인기가 줄어들긴 했지만 송가인, 임영웅 같은 가수들의 노래에 열광하는 우리의 모습은 트로트가 아직 건재함을, 아니 오히려 이 시대에 더욱 잘 부합하는 음악이라는 생각을 하게 만든다."
        )

    def tearDown(self):
        Magazine.objects.all().delete()

    def test_magazine_get_success(self):
        client = Client()
        response = client.get('/music/magazine')
        self.assertEqual(response.json(),
            {
                 "magazine_list": [
                     {
                         "magazine_id"               : 1,
                         "badge"                     : "https://music-phinf.pstatic.net/20190702_287/1562066500033t4gp0_PNG/icon_pick.png",
                         "release_date"              : "2020-03-10",
                         "title"                     : "이주의 디깅 #49 \\n임영웅",
                         "description"               : "지상파 이외 채널 프로그램으로는 가장 높은 시청률이라는 대기록을 세운 ‘내일은 미스터트롯’이 많은 사랑을 받고 있다. 갑자기 웬 트로트 붐이냐?라고 하는 사람들도 있겠지만 사실 트로트는 아주 오래전부터 우리와 함께해 왔다. 세대가 바뀌면서 인기가 줄어들긴 했지만 송가인, 임영웅 같은 가수들의 노래에 열광하는 우리의 모습은 트로트가 아직 건재함을, 아니 오히려 이 시대에 더욱 잘 부합하는 음악이라는 생각을 하게 만든다."
                      }
                 ]
            }
        )
        self.assertEqual(response.status_code, 200)

class NewsTest(TestCase):
    def setUp(self):
        client = Client()
        News.objects.create(
            id                  = 1,
            thumbnail           = "https://music-phinf.pstatic.net/20200313_263/1584075337504GK5eL_JPEG/%B4%BA%BD%BA%C5%AC%B8%AE%C7%CE-%B9%E6%C5%BA%BC%D2%B3%E2%B4%DC.jpg",
            main_text           = "방탄소년단이 정규 4집으로 한국 가수 최다 판매 기록을 세웠습니다.",
            news_link           = "https://www.ytn.co.kr/_sn/1408_202003121136020500"
        )

    def tearDown(self):
        News.objects.all().delete()

    def test_magazine_get_success(self):
        client = Client()
        response = client.get('/music/news')
        self.assertEqual(response.json(),
            {
                "news_list": [
                    {
                        "news_id"         : 1,
                        "thumbnail"       : "https://music-phinf.pstatic.net/20200313_263/1584075337504GK5eL_JPEG/%B4%BA%BD%BA%C5%AC%B8%AE%C7%CE-%B9%E6%C5%BA%BC%D2%B3%E2%B4%DC.jpg",
                        "main_text"       : "방탄소년단이 정규 4집으로 한국 가수 최다 판매 기록을 세웠습니다.",
                        "news_link"       : "https://www.ytn.co.kr/_sn/1408_202003121136020500"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class RecommendationTest(TestCase):
    def setUp(self):
        client = Client()
        Recommendation.objects.create(
            id                      = 2,
            title                   = "FRIDAY DISCO",
            sub_title               = "VIBE",
            main_image              = "https://music-phinf.pstatic.net/20191121_189/1574328239813ldKsO_PNG/VIBE_%B0%F8%C5%EB_FridayDisco.png",
            description             = "주말을 향해 달려온 당신을 위한 흥을 돋우는 경쾌한 리듬! 지루할 틈 없이 리듬을 타게 되는 디스코, 펑키 음악과 함께 신나는 주말을 맞이하세요. 디스코 음악을 사랑하는 사장님이 계신 카페 '파티션 WSC'에서 선곡한 이 플레이리스트는 매주 업데이트됩니다. 업데이트되면 수록곡이 바뀌니, 마음에 드는 곡은 좋아요를 눌러 보관함에 담아두세요."            
        )

    def tearDown(self):
        News.objects.all().delete()

    def test_magazine_get_success(self):
        client = Client()
        response = client.get('/music/recommendation')
        self.assertEqual(response.json(),
            {               
                "recommendation_list": [
                    {
                        "recommendation_id" : 2,
                        "title"             : "FRIDAY DISCO",
                        "sub_title"         : "VIBE",
                        "main_image"        : "https://music-phinf.pstatic.net/20191121_189/1574328239813ldKsO_PNG/VIBE_%B0%F8%C5%EB_FridayDisco.png",
                        "description"       : "주말을 향해 달려온 당신을 위한 흥을 돋우는 경쾌한 리듬! 지루할 틈 없이 리듬을 타게 되는 디스코, 펑키 음악과 함께 신나는 주말을 맞이하세요. 디스코 음악을 사랑하는 사장님이 계신 카페 '파티션 WSC'에서 선곡한 이 플레이리스트는 매주 업데이트됩니다. 업데이트되면 수록곡이 바뀌니, 마음에 드는 곡은 좋아요를 눌러 보관함에 담아두세요."
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class LatestAlbumTest(TestCase):
    def setUp(self):
        client = Client()
        Album.objects.create(
            id                      = 1,
            name                    = "Lovely Sweet Heart",
            image                   = "https://musicmeta-phinf.pstatic.net/album/000/060/60001.jpg?type=r480Fll&v=20191212192801",
            release_date            = "2010-01-01"
                        
        )

        Album.objects.create(
            id                      = 2,
            name                    = "전설",
            image                   = "https://musicmeta-phinf.pstatic.net/album/002/923/2923941.jpg?type=r480Fll&v=20200218131711",
            release_date            = "2009-01-01"
        )

        Artist.objects.create(
            id                      = 1,
            name                  = "씨야(SeeYa)"
        )

        Artist.objects.create(
            id                      = 2,
            name                  = "잔나비"
        )

        ArtistAlbum.objects.create(
            artist                  = Artist.objects.get(id = 1),
            album                   = Album.objects.get(id = 1)
        )

        ArtistAlbum.objects.create(
            artist                  = Artist.objects.get(id = 2),
            album                   = Album.objects.get(id = 2)
        )
        

    def tearDown(self):
        Artist.objects.all().delete()
        Album.objects.all().delete()
        ArtistAlbum.objects.all().delete()

    def test_latestalbum_get_success(self):
        client = Client()
        response = client.get('/music/latestalbum')
        self.assertEqual(response.json(),
            {
                "latest_album_list" : [                    
                    {
                        'album_id'        :  1,
                        'album_name'      :  "Lovely Sweet Heart",
                        'album_image'     :  "https://musicmeta-phinf.pstatic.net/album/000/060/60001.jpg?type=r480Fll&v=20191212192801",
                        'album_artist_name'     :  ["씨야(SeeYa)"]
                    },
                    {
                        'album_id'         : 2,
                        'album_name'      : "전설",
                        'album_image'     : "https://musicmeta-phinf.pstatic.net/album/002/923/2923941.jpg?type=r480Fll&v=20200218131711",
                        'album_artist_name'     : ["잔나비"]           
                    }                                        
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    

