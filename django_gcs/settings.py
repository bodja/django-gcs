from django.conf import settings


DEFAULTS = {
    'bucket': None,
    'project': '',
    'credentials': None,
    'http': None
}


def make_settings():
    defaults = DEFAULTS.copy()
    defaults.update(getattr(settings, 'DJANGO_GCS', {}))
    return defaults


gcs_settings = make_settings()
