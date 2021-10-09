"""Plato serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from backend_test.menus.models import Plato
import uuid

class PlatoModelSerializer(serializers.ModelSerializer):
    """Plato model serializer."""

    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        """Meta class."""

        model = Plato
        fields = (
            'nombre', 'descripcion',
            'observaciones', 'id'
        )
        read_only_fields = (
            'id',
        )

    def create(self, data):
        return Plato.objects.create(**data)


class CrearPlatoSerializer(serializers.Serializer):
    """Crear plato serializer"""
    pass