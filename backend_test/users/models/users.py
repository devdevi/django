"""Model de Usuarios"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from backend_test.utils.models import BaseModel

class User(BaseModel, AbstractUser):
    """Modelo Usuarios

    Extiende desde django AbstractUser y añade campos extras
    requeridos para la aplicacion.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={
            'unique': 'El usuario ya existe'
        },
        max_length=254)

    REQUIRED_FIELDS = ['email']

    is_employed = models.BooleanField(
        'employed status',
        default=True,
        help_text=(
            'ayudar a distinguir fácilmente a los usuarios y realizar consultas',
            'Los empleados son el principal tipo de usuario'
        )
    )

    is_admin = models.BooleanField(
        'Nora administradora',
        default=False,
        help_text=(
            'Usuario encargado de ver las solicitudes de los empleados y actualizar el menu del dia.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text="Cambia su valor a True cuando el usuario haya verificado su dirección de correo electrónico"
    )

    def __str__(self) -> str:
        """Retorna username"""

        return self.username

    def get_short_name(self):
        """Retorna username"""
        return self.username