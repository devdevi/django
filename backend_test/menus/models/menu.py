"""Modelo Menus"""

# Django
from django.db import models
import uuid

# Utilities
from backend_test.utils.models import BaseModel

# Models
from backend_test.menus.models import Plato


class Menu(models.Model):
    """Menu model.

    Un menu es un listado de menus (opciones/platos) diarias
    en donde los clientes puedes seleccionar su menu del dia
    disponible hasta las 11 am.
    """
    nombre = models.CharField(max_length=100, null=True)
    # opciones = models.ManyToManyField(Plato)
    fecha = models.DateTimeField(
        'Fecha de creacion',
        auto_now_add=False,
        help_text='Dia de disponibilidad del menu'
    )
    menus_solicitados = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(
        'Menu activo',
        default=False,
        help_text='La seleccion del menu solo estara disponible hasta las 11 de la mañana.'
    )

    """Solo permite la seleccion de menu del dia hasta las 11 de la mañana """

    class Meta:
        """Meta option."""

        get_latest_by = 'fecha'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre}-{self.fecha}"
