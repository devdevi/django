"""Model Empleados"""

# Django
from django.db import models


# Utilities
import uuid
from backend_test.utils.models import BaseModel


class Plato(BaseModel):
    """Model de plato

    Un plato es una opcion disponible en el menu
    permite enviar preferencias en la seleccion del mismo
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField('descripcion', max_length=500)
    observaciones = models.CharField(
        'especificar personalizaciones',
        max_length=500,
        null=True,
        blank=True,
        help_text="Permite al empleado personalizar y enviar sus preferencias")
    postre = models.BooleanField(
        'postre',
        default=True,
    )
    ensalada = models.BooleanField(
        'ensalada',
        default=True,
    )
    # menu = models.OneToOneField(
    #     "menus.Menu",
    #     on_delete=models.CASCADE)

    """Validar si el menu esta disponble antes de aceptar la solicitud"""

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
