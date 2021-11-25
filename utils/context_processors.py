from django.utils.timezone import now


def tz_now(request):
    return {'now': now()}
