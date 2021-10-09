"""Vista Platos (opciones)"""

# Django
from backend_test.menus.models.plato import Plato
from django.http import HttpResponse

# Django rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Serlializers
from backend_test.menus.serializer import PlatoModelSerializer


@api_view(['POST'])
def lista_platos(request):
    """Listado platos"""
    platos = Plato.objects.all()
    data = PlatoModelSerializer(platos, many=True)
    # data = []
    # for plato in platos:
    #     serializer = PlatoModelSerializer(plato)
    #     data.append(serializer)
    return Response(data.data)


@api_view(['POST'])
def crear_plato(request):
    """crear plato"""

    serializer = PlatoModelSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    plato = serializer.save()
    return Response(PlatoModelSerializer(plato).data)
