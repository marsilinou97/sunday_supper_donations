from .models import RegistrationToken
import datetime


def validate_token(token):
    error_msg = ""
    if not token:
        error_msg = "Token can't be empty."
    else:
        token_obj = RegistrationToken.objects.get(token=token)

        if not token_obj:
            error_msg = "Token does not exist."

        if not token_obj.active:
            error_msg = "Token is inactive."

        date_created = token_obj.date_created
        token_expiration_period = token_obj.expiration_period

        if datetime.date.today() > date_created + datetime.timedelta(days=token_expiration_period):
            error_msg = "Token expired."

    return error_msg
#
