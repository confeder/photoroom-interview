from rest_framework import renderers


class VendoredJSONRenderer(renderers.JSONRenderer):
    media_type = "application/vnd.photoroom+json"
