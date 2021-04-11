import bleach
from django.http import JsonResponse


def __remove_html_tags(data, strip=True, tags=[], attributes={}, protocols=[]):
    bleach.clean(data, strip=strip, tags=tags, attributes=attributes, protocols=protocols)
    data.replace("{", "").replace("}", "").replace("%", "")
    return data


def remove_html_tags(data, strip=True, tags=[], attributes={}, protocols=[]):
    """
    :param data: dict or str
    :param strip: boolean to strip strings after striping tags
    :param tags: allowed tags
    :param attributes: allowed attrs
    :param protocols: allowed protocols
    :return: cleaned data
    """
    if type(data) == dict:
        for k, v in data.items():
            if type(v) == str:
                data[k] = __remove_html_tags(v, strip=strip, tags=tags, attributes=attributes, protocols=protocols)
    # Allow more types (any str like type) if needed
    elif type(data) == str:
        data = __remove_html_tags(data)

    else:
        raise TypeError(f"Expected dict or str type, got {type(data)} instead")

    return data


class FailedJsonResponse(JsonResponse):
    def __init__(self, data):
        super().__init__(data)
        self.status_code = 400
