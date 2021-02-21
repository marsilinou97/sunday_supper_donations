from .models import RegistrationToken


def token_exists(token):
    return RegistrationToken.objects.filter(token=token).exists()
