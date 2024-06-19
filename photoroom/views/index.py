from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(status=403, content="Nothing here.", content_type="text/plain")
