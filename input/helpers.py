import bleach


def remove_html_tags(data):
    for k, v in data.items():
        if type(v) == str:
            data[k] = bleach.clean(v, strip=True, tags=[], attributes={}, protocols=[])
            data[k] = data[k].replace("{", "").replace("}", "").replace("%", "")
    return data
