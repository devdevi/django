"""Model Empleados"""

# Django
from django.db import models


# Utilities
from backend_test.utils.models import BaseModel

# Model
from backend_test.menus.models import Plato
class Employee(BaseModel):
    """Modelo empleado


    Tiene datos del usuario y registros de  menus solicitados
    """
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE)

    biography = models.TextField(max_length=500, blank=True)

    menus_taken = models.PositiveIntegerField(default=0)
    menus = models.ManyToManyField(Plato)
