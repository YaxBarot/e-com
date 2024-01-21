import jwt
import datetime

from django.conf import settings
from django.db.models import Q
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from common.messages import TOKEN_EXPIRED
from custom_security.models import AdminAuthTokens
from e_commerce.settings import JWT_ALGORITHM, JWT_SECRET, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from .serializers import AdminAuthTokenSerializer
from administrator.models import Admin


def save_admin_auth_tokens(authentication_tokens):
    admin_auth_token_serializer = AdminAuthTokenSerializer(data=authentication_tokens)
    if admin_auth_token_serializer.is_valid():
        admin_auth_token_serializer.save()


def get_admin_authentication_tokens(admin):
    access_token = jwt.encode({"admin_id": admin.admin_id,
                               "email": admin.email,
                               "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME,
                               "type": "access"},
                              settings.JWT_SECRET,
                              algorithm=settings.JWT_ALGORITHM)

    refresh_token = jwt.encode({"admin_id": admin.admin_id,
                                "email": admin.email,
                                "exp": datetime.datetime.now(
                                    tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME,
                                "type": "refresh"},
                               settings.JWT_SECRET,
                               algorithm=settings.JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expiry": settings.ACCESS_TOKEN_LIFETIME,
        "refresh_token_expiry": settings.REFRESH_TOKEN_LIFETIME
    }


def admin_token_decode(token):
    try:
        claims = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)

        if not AdminAuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).exists():
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        if "admin_id" not in claims:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        employee = Admin.objects.get(admin_id=claims["admin_id"],
                                     email=claims["email"],
                                     is_deleted=False)

        return employee, claims

    except Admin.DoesNotExist as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)

    except AuthenticationFailed as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except jwt.exceptions.InvalidSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except Exception as e:
        raise e


class AdminJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            if "authorization" not in request.headers:
                raise PermissionDenied()

            token = request.headers.get("authorization").split(" ")[1]

            return admin_token_decode(token)

        except PermissionDenied as e:
            raise PermissionDenied()

        except AuthenticationFailed as e:
            raise AuthenticationFailed(e.detail)

        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        except jwt.exceptions.DecodeError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)
