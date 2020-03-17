import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibe.settings')

import django
django.setup()

from datetime import date

import random
import csv
from music.models import *

#artist
print("artist")
def add_artist():
    with open('./upload/artist.csv', mode='r') as artist_lists:
        reader = csv.reader(artist_lists, delimiter=',')

        for artist in list(reader)[1:]:
            debut = artist[2]
            birth = artist[5]
            if artist[2] == "":
                debut = date(1900,1,1)
            if artist[5] == "":
                birth = date(1900,1,1)

            Artist(
                    name             = artist[0],
                    image            = artist[1],
                    debut_date       = debut,
                    birth_country    = artist[3],
                    nationality      = artist[4],
                    birth_date       = birth,
                    gender           = artist[6],
                    is_group         = artist[7],
                    ).save()
add_artist()

# video
print("video")
def add_video():
    with open('./upload/video.csv', mode='r') as video_lists:
        reader = csv.reader(video_lists, delimiter=',')

        for video in list(reader)[1:]:
            print(video)
            Video.objects.create(
                    name             = video[0],
                    main_image       = video[1],
                    release_date     = video[2]                    
                    )

add_video()

#album
print("album")
def add_album():
    with open('./upload/album.csv', mode='r') as album_lists:
        reader = csv.reader(album_lists, delimiter=',')

        for album in list(reader)[1:]:
            print(album)
            Album.objects.create(
                    name             = album[0],
                    image            = album[1],
                    release_date     = album[2], 
                    description      = album[3],
                    production_name  = album[4],
                    agency_name      = album[5],
                    is_regular       = album[6]                   
                    )

add_album()

#music
print("music")
def add_music():
    with open('./upload/music.csv', mode='r') as music_lists:
        reader = csv.reader(music_lists, delimiter=',')

        for music in list(reader)[1:]:
            print(music)
            a = ['00:03:40', '00:02:30', '00:03:12', '00:01:48', '00:02:19', '00:04:08']
            if music[7] == '':
                play = random.choice(a)
            Music.objects.create(
                album_id      = music[0],
                name          = music[1],
                track_number  = music[2],
                writer        = music[3],
                composer      = music[4],
                arranger      = music[5],
                lyrics        = music[6],
                play_time     = play
                    )

add_music()

#genre
print("genre")
def add_genre():
    with open('./upload/genre.csv', mode='r') as genre_lists:
        reader = csv.reader(genre_lists, delimiter=',')

        for genre in list(reader)[1:]:
            print(genre)
            Genre.objects.create(
                    name             = genre[0],                    
                    )

add_genre()

# artist_genre
print("artist_genre")
def add_artist_genre():
    with open('./upload/artist_genre.csv', mode='r') as artist_genre_lists:
        reader = csv.reader(artist_genre_lists, delimiter=',')

        for artist_genre in list(reader)[1:]:
            print(artist_genre)
            ArtistGenre.objects.create(
                    artist_id             = artist_genre[0],
                    genre_id              = artist_genre[1]
                    )

add_artist_genre()

# genre_album
print("genre_album")
def add_genre_album():
    with open('./upload/genre_album.csv', mode='r') as genre_album_lists:
        reader = csv.reader(genre_album_lists, delimiter=',')

        for genre_album in list(reader)[1:]:
            print(genre_album)
            GenreAlbum.objects.create(
                    genre_id              = genre_album[0],
                    album_id              = genre_album[1]                   
                    )

add_genre_album()

# similar_artist
print("similar_artist")
def add_similar_artist():
    with open('./upload/similar_artist.csv', mode='r') as similar_artist_lists:
        reader = csv.reader(similar_artist_lists, delimiter=',')

        for similar_artist in list(reader)[1:]:
            print(similar_artist)
            SimilarArtist.objects.create(
                    base_artist_id              = similar_artist[0],
                    similar_artist_id           = similar_artist[1]                   
                    )

add_similar_artist()

# artist_album
print("artist_album")
def add_artist_album():
    with open('./upload/artist_album.csv', mode='r') as artist_album_lists:
        reader = csv.reader(artist_album_lists, delimiter=',')

        for artist_album in list(reader)[1:]:
            print(artist_album)
            ArtistAlbum.objects.create(
                    artist_id              = artist_album[0],
                    album_id               = artist_album[1]
                    )

add_artist_album()

# artist_music
print("artist_music")
def add_artist_music():
    with open('./upload/artist_music.csv', mode='r') as artist_music_lists:
        reader = csv.reader(artist_music_lists, delimiter=',')

        for artist_music in list(reader)[1:]:
            print(artist_music)
            ArtistMusic.objects.create(
                    artist_id              = artist_music[0],
                    music_id               = artist_music[1]

                    )

add_artist_music()

# artist_video
print("artist_video")
def add_artist_video():
    with open('./upload/artist_video.csv', mode='r') as artist_video_lists:
        reader = csv.reader(artist_video_lists, delimiter=',')

        for artist_video in list(reader)[1:]:
            print(artist_video)
            ArtistVideo.objects.create(
                    artist_id              = artist_video[0],
                    video_id               = artist_video[1]
                    )

add_artist_video()

#Recommendation
print("recommendation")
def add_recommendation():
    with open('./upload/recommendation.csv', mode='r') as recommendation_lists:
        reader = csv.reader(recommendation_lists, delimiter=',')

        for recommendation in list(reader)[1:]:
            print(recommendation)
            Recommendation.objects.create(
                    title              = recommendation[0],
                    sub_title          = recommendation[1],
                    main_image         = recommendation[2],
                    description        = recommendation[3]
                    )

add_recommendation()

#RecommendationMusic
print("recommendation_music")
def add_recommendation_music():
    with open('./upload/recommendation_music.csv', mode='r') as recommendation_music_lists:
        reader = csv.reader(recommendation_music_lists, delimiter=',')

        for recommendation_music in list(reader)[1:]:
            print(recommendation_music)
            RecommendationMusic.objects.create(
                recommendation_id           = recommendation_music[0],
                music_id                    = recommendation_music[1]                
                )

add_recommendation_music()

#News
print("news")
def add_news():
    with open('./upload/news.csv', mode='r') as news_lists:
        reader = csv.reader(news_lists, delimiter=',')

        for news in list(reader)[1:]:
            print(news)
            News.objects.create(
                thumbnail              = news[0],
                main_text              = news[1],
                news_link              = news[2]
                )

add_news()

#Magazine
print("magazine")
def add_magazine():
    with open('./upload/magazine.csv', mode='r') as magazine_lists:
        reader = csv.reader(magazine_lists, delimiter=',')

        for magazine in list(reader)[1:]:
            print(magazine)
            Magazine.objects.create(
                badge                  = magazine[0],
                thumbnail              = magazine[1],
                release_date           = magazine[2],
                title                  = magazine[3],
                description            = magazine[4]
                )

add_magazine()


# MusicMagazine
print("music_magazine")
def add_magazine():
    with open('./upload/music_magazine.csv', mode='r') as music_magazine_lists:
        reader = csv.reader(music_magazine_lists, delimiter=',')

        for music_magazine in list(reader)[1:]:
            print(music_magazine)
            MusicMagazine.objects.create(
                music_id               = music_magazine[0],
                magazine_id            = music_magazine[1]                
                )

add_magazine()

# Station
def add_station():
    with open('./upload/station.csv', mode='r') as station_lists:
        reader = csv.reader(station_lists, delimiter=',')

        for station in list(reader):
            print(station)
            Station(
                name = station[0],
            ).save()
add_station()

# Theme
def add_theme():
    with open('./upload/themes.csv', mode='r') as station_lists:
        reader = csv.reader(station_lists, delimiter=',')

        for station in list(reader):
            print(station)
            Theme(
                category = station[0],
                name     = station[1],
                creator  = station[2],
                charge   = station[3],
                main_image = station[4]
            ).save()
add_theme()

# StationTheme
def add_station_theme():
    with open('./upload/theme_details.csv', mode='r') as station_lists:
        reader = csv.reader(station_lists, delimiter=',')

        for station in list(reader):
            print(station)
            StationTheme(
                station_id = station[0],
                theme_id   = station[1],
                image      = station[2],
            ).save()
add_station_theme()

# StationTheme_2
def add_station_fix_theme():
    with open('./upload/fix_theme.csv', mode='r') as station_lists:
        reader = csv.reader(station_lists, delimiter=',')

        Theme(
            category = 'GENRE',
            name = 'GENRE',
            creator = 'VIBE',
            charge = '무료'
        ).save()

        for station in list(reader):
            print(station)
            StationTheme(
                station_id = station[0],
                theme_id   = station[1],
                image      = station[2],
            ).save()
add_station_fix_theme()

# Station_Music
def add_station_music():
    with open('./upload/station_music.csv', mode='r') as station_lists:
        reader = csv.reader(station_lists, delimiter=',')

        for station in list(reader)[1:]:
            print(station)
            StationMusic(
                music_id   = station[0],
                station_id = station[1],
            ).save()
add_station_music()

