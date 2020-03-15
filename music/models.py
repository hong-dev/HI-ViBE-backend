from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length = 25)

    class Meta:
        db_table = 'genres'

class Album(models.Model):
    name             = models.CharField(max_length = 50)
    image            = models.URLField(max_length = 2000, null = True)
    release_date     = models.DateField(null = True)
    description      = models.TextField(null = True)
    production_name  = models.CharField(max_length = 200, null = True)
    agency_name      = models.CharField(max_length = 200, null = True)
    is_regular       = models.BooleanField(default = False)
    genre            = models.ManyToManyField('Genre', through = 'GenreAlbum')

    class Meta:
        db_table = 'albums'

class GenreAlbum(models.Model):
    genre = models.ForeignKey('Genre', on_delete = models.SET_NULL, null = True)
    album = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'genre_albums'

class Music(models.Model):
    album            = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)
    name             = models.CharField(max_length = 100)
    content          = models.URLField(max_length = 2000)
    track_number     = models.IntegerField(default = 1)
    writer           = models.CharField(max_length = 600, null = True)
    composer         = models.CharField(max_length = 600, null = True)
    arranger         = models.CharField(max_length = 600, null = True)
    lyrics           = models.TextField(null = True)
    play_time        = models.TimeField(null = True)

    class Meta:
        db_table = 'musics'

class Video(models.Model):
    music        = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)
    name         = models.CharField(max_length = 300)
    main_image   = models.URLField(max_length = 2000)
    content      = models.URLField(max_length = 2000, null = True)
    release_date = models.DateField()
    views        = models.IntegerField(null = True)

    class Meta:
        db_table = 'videos'

class Artist(models.Model):
    name             = models.CharField(max_length = 100)
    image            = models.URLField(max_length = 2000, null = True)
    debut_date       = models.DateField(null = True)
    birth_country    = models.CharField(max_length = 50, null = True)
    nationality      = models.CharField(max_length = 50, null = True)
    birth_date       = models.DateField(null = True)
    gender           = models.CharField(max_length = 10, null = True)
    is_group         = models.BooleanField(default = False)
    genre            = models.ManyToManyField('Genre', through = 'ArtistGenre')
    album            = models.ManyToManyField('Album', through = 'ArtistAlbum')
    music            = models.ManyToManyField('Music', through = 'ArtistMusic')
    video            = models.ManyToManyField('Video', through = 'ArtistVideo')
    similar_ralation = models.ManyToManyField('self', through = 'SimilarArtist', symmetrical = False)

    class Meta:
        db_table = 'artists'

class SimilarArtist(models.Model):
    base_artist    = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True, related_name = 'base_artist')
    similar_artist = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True, related_name = 'similar_artist')

    class Meta:
        unique_together = ('base_artist', 'similar_artist')
        db_table        = 'similar_artists'

class ArtistGenre(models.Model):
    artist = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True)
    genre  = models.ForeignKey('Genre', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artist_genres'

class ArtistAlbum(models.Model):
    artist = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True)
    album  = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artist_albums'

class ArtistMusic(models.Model):
    artist = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True)
    music  = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artist_musics'

class ArtistVideo(models.Model):
    artist = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True)
    video  = models.ForeignKey('Video', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artist_videos'

class Recommendation(models.Model):
    title       = models.CharField(max_length = 200)
    sub_title   = models.CharField(max_length = 100)
    main_image  = models.URLField(max_length = 2000)
    description = models.TextField()
    music       = models.ManyToManyField('Music', through = 'RecommendationMusic')

    class Meta:
        db_table = 'recommendations'

class RecommendationMusic(models.Model):
    recommendation = models.ForeignKey('Recommendation', on_delete = models.SET_NULL, null = True)
    music          = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'recommendation_musics'

class News(models.Model):
    artist    = models.ForeignKey('Artist', on_delete = models.SET_NULL, null = True)
    thumbnail = models.URLField(max_length = 2000)
    main_text = models.TextField()
    news_link = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'news'

class Magazine(models.Model):
    badge        = models.URLField(max_length = 2000, null = True)
    thumbnail    = models.URLField(max_length = 2000)
    release_date = models.DateField()
    title        = models.TextField()
    description  = models.TextField()
    content      = models.TextField()
    music        = models.ManyToManyField('Music', through = 'MusicMagazine')

    class Meta:
        db_table = 'magazines'

class MusicMagazine(models.Model):
    music    = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)
    magazine = models.ForeignKey('Magazine', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'music_magazines'

class Station(models.Model):
    name        = models.CharField(max_length = 30)
    description = models.TextField(null = True)
    music       = models.ManyToManyField('Music', through = 'StationMusic')
    theme       = models.ManyToManyField('Theme', through = 'StationTheme')

    class Meta:
        db_table = 'stations'

class StationMusic(models.Model):
    station = models.ForeignKey('Station', on_delete = models.SET_NULL, null = True)
    music   = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'station_musics'

class Theme(models.Model):
    category   = models.CharField(max_length = 50)
    name       = models.CharField(max_length = 50)
    creator    = models.CharField(max_length = 30)
    charge     = models.CharField(max_length = 10)
    main_image = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'themes'

class StationTheme(models.Model):
    station = models.ForeignKey('Station', on_delete = models.SET_NULL, null = True)
    theme   = models.ForeignKey('Theme', on_delete = models.SET_NULL, null = True)
    image   = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'station_themes'
