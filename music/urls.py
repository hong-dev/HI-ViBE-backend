from .views import (
    StationView,
    ThemeView,
    StationThemeView,
    MagazineView,
    MusicMagazineView,
    NewsView,
    RecommendationView,
    LatestAlbumView
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
    path('/latestalbum', LatestAlbumView.as_view())
]
