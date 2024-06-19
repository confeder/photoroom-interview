from django import forms
from django.contrib import admin
from django.contrib.admin import site as admin_site
from django.forms import widgets
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from photoroom.models import ColorPallete

admin_site.site_header = "Photoroom admin"
admin_site.site_title = "Photoroom admin"


class ColorPalleteAdminForm(forms.ModelForm):
    class Meta:
        model = ColorPallete
        fields = ["name", "colors", "owner"]
        widgets = {"name": widgets.TextInput}


@admin.register(ColorPallete, site=admin_site)
class ColorPalleteAdmin(admin.ModelAdmin, DynamicArrayMixin):
    form = ColorPalleteAdminForm
