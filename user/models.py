from music.models import Genre, Artist, Album, Music, Station

from django.db import models

class Membership(models.Model):
    name = models.CharField(max_length = 40)

    class Meta:
        db_table = 'memberships'

class User(models.Model):
    membership  = models.ForeignKey('Membership', on_delete = models.SET_NULL, null = True)
    naver_id    = models.CharField(max_length = 20)
    nickname    = models.CharField(max_length = 20)
    name        = models.CharField(max_length = 20)
    email       = models.CharField(max_length = 50)
    image       = models.URLField(max_length = 2000)
    gender      = models.CharField(max_length = 5)
    birthday    = models.DateField(null = True)
    expiry_date = models.DateField(null = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

class Playlist(models.Model):
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    name       = models.CharField(max_length = 50)
    music      = models.ManyToManyField(Music, through = 'PlaylistMusic')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'playlists'

class PlaylistMusic(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete = models.SET_NULL, null = True)
    genre    = models.ForeignKey(Genre, on_delete = models.SET_NULL, null = True)
    artist   = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True)
    music    = models.ForeignKey(Music, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'playlist_musics'

class MusicHistory(models.Model):
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    music      = models.ForeignKey(Music, on_delete = models.SET_NULL, null = True)
    artist     = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True)
    album      = models.ForeignKey(Album, on_delete = models.SET_NULL, null = True)
    count      = models.IntegerField()
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'music_histories'

class StationHistory(models.Model):
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    station    = models.ForeignKey(Station, on_delete = models.SET_NULL, null = True)
    count      = models.IntegerField()
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'station_histories'

class MusicLike(models.Model):
    user  = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    music = models.ForeignKey(Music, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'music_likes'

class ArtistLike(models.Model):
    user   = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    artist = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artist_likes'

class AlbumLike(models.Model):
    user  = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    album = models.ForeignKey(Album, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'album_likes'
