import jwt
import json
import requests

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from vibe.settings          import SECRET_KEY
from .models                import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY['secret'], algorithms = 'HS256')
            user         = User.objects.get(naver_id = payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN" }, status = 400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER" }, status = 400)
        except KeyError:
            JsonResponse({"message": "INVALID_KEY" }, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper

def check_login(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            try:
                decode = jwt.decode(access_token, SECRET_KEY['secret'], algorithms = ['HS256'])
                user = User.objects.get(naver_id = decode['user_id'])

                request.user = user

            except jwt.DecodeError:
                return JsonResponse({"message": "INVALID_TOKEN"}, status = 403)
            except User.DoesNotExist:
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

        else:
            request.user = None

        return func(self, request, *args, **kwargs)
    return wrapper
