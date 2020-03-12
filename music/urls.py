from .views import StationView, ThemeView, StationThemeView

from django.urls import path

urlpatterns = [
    path('/station', StationView.as_view()),
    path('/station/theme', ThemeView.as_view()),
    path('/station/theme<int:theme_id>', StationThemeView.as_view())
]
