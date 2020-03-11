from .views import NaverSignInView

from django.urls import path

urlpatterns = [
    path('/naver_auth', NaverSignInView.as_view())
]
