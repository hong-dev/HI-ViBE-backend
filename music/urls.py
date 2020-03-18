from .views import (
    StationView,
    ThemeView,
    StationThemeView,
    MagazineView,
    MusicMagazineView,
    NewsView,
    RecommendationView,
    LatestAlbumView,
    RecommendationMusicView,
    StationMusicView,
    AlbumMusicView,
    ArtistMusicView,
    MusicPlayView,
    MusicView,
    ArtistView,
    AlbumListView,
    MusicStreamView,
    MusicSearchView
)

from django.urls import path

urlpatterns = [
    path('/station', StationView.as_view()),
    path('/station/theme', ThemeView.as_view()),
    path('/station/theme<int:theme_id>', StationThemeView.as_view()),
    path('/magazine', MagazineView.as_view()),
    path('/magazine/<int:magazine_id>', MusicMagazineView.as_view()),
    path('/news', NewsView.as_view()),
    path('/recommendation', RecommendationView.as_view()),
    path('/latestalbum', LatestAlbumView.as_view()),
    path('/recommendation_music/<int:recommendation_id>', RecommendationMusicView.as_view()),
    path('/station_music/<int:station_id>', StationMusicView.as_view()),
    path('/album_music/<int:album_id>', AlbumMusicView.as_view()),
    path('/artist_music/<int:artist_id>', ArtistMusicView.as_view()),
    path('/albums/artist<int:artist_id>', AlbumListView.as_view()),
    path('/track/<int:music_id>', MusicView.as_view()),
    path('/artist/<int:artist_id>', ArtistView.as_view()),
    path('/<int:music_id>/play', MusicPlayView.as_view()),
    path('/stream/<int:music_id>', MusicStreamView.as_view()),
    path('/search', MusicSearchView.as_view())
]
