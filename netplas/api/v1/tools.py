from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from profile.models import UserProfile


def create_profile(user, params):
    try:
        if user and user.is_authenticated:
            raise Exception("Zaten giriş yapmış durumdasınız.")
        if UserProfile.objects.filter(email=params["user"]["email"]).exists():
            raise Exception('Lütfen başka bir e-posta adresi kullanın.')
        password = params["user"]['password']
        password_again = params["user"]['password_again']
        if password != password_again:
            raise Exception('Girdiğiniz parolalar aynı değil. Lütfen tekrar deneyiniz..')
        else:
            try:
                password_validation.validate_password(password)
            except ValidationError:
                raise Exception('Girilen parololar doğru değil.')
            params["user"]["password"] = make_password(password)
            params["user"].pop("password_again")
            profile = UserProfile(**params["user"])
            profile.save()
    except Exception as ex:
        raise Exception(ex)


def check_user_is_valid(user, **kwargs):  # Must be one signal token validation
    if user is None:
        raise Exception("E-posta yada parolanız hatalı, lütfen tekrar deneyiniz.")
