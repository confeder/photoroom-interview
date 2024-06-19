from colorfield.fields import ColorField
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class ColorPallete(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(name="photoroom_colorpallete_uniq", fields=["name"])
        ]

    name = models.TextField(max_length=255, null=False, blank=False)
    colors = ArrayField(ColorField(format="hex"), blank=True, null=False)

    owner = models.ForeignKey(
        "auth.Group", on_delete=models.CASCADE, related_name="color_palletes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
