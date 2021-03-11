from django.core.exceptions import ValidationError
from django.utils.translation import gettext

class UpperCaseValidator:
    def __init__(self):
        self.upper_case_letters = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def validate(self, password, user=None):
        for i in range(0,len(password)):
            if password[i] in self.upper_case_letters:
                return None

        raise ValidationError(
            gettext("Password must contain at least 1 upper case letter"),
            code='no_upper_case_letters',
            params={}
        )

    def get_help_text(self):
        return gettext("Password must contain at least 1 upper case letter")

class LowerCaseValidator:
    def __init__(self):
        self.lower_case_letters = tuple("abcdefghijklmnopqrstuvwxyz")

    def validate(self, password, user=None):
        for i in range(0,len(password)):
            if password[i] in self.lower_case_letters:
                return None

        raise ValidationError(
            gettext("Password must contain at least 1 lower case letter"),
            code='no_lower_case_letters',
            params={}
        )

    def get_help_text(self):
        return gettext("Password must contain at least 1 lower case letter")

class SpecialCharacterValidator:
    def __init__(self):
        self.special_case_letters = tuple("~!@#$%^&*_-+=`:;")

    def validate(self, password, user=None):
        for i in range(0, len(password)):
            if password[i] in self.special_case_letters:
                return None

        raise ValidationError(
            gettext("Password must contain at least 1 special case letter from ~!@#$%^&*_-+=`:;"),

            code='no_special_case_letters',
            params={})

    def get_help_text(self):
        return gettext("Password must contain at least 1 special case letter from ~!@#$%^&*_-+=`:;")
