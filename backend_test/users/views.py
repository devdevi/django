"""Vista Usuarios"""

# Django
from django.http import HttpResponse

# Django rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

# +ViewSet: cuando usamos la mayoria de operaciones crud en un modelo

# +Generics: cuando solo desee permitir algunas operaciones en un modelo

# +ApiView :cuando desee personalizar completamente las operaciones de un modelo.

# espero les sirva como una guia ,

