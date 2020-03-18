from .views import NaverSignInView, LikeAlbumView

from django.urls import path

urlpatterns = [
    path('/naver_auth', NaverSignInView.as_view()),
    path('/album', LikeAlbumView.as_view())
]
