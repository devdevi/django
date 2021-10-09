from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from django.http import JsonResponse
import requests
import time
from rest_framework import status
from rest_framework.response import Response

import requests
import json
SLACK = "https://hooks.slack.com/services/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"


@api_view(["GET", "HEAD", "POST"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def healthz(request, *args, **kwargs):
    print(request)
    external_api_view(request)
    return Response(status=200)


def external_api_view(request):
    print("hola")
    # // Puede ser una de 'good' U02EGEYKUP9, 'warning', 'danger', o cualquier código de color hexadecimal
    if request.method == "GET":
        url = SLACK
        channel = "visidevi"
        payload = {
            "channel": f'@{channel}',
            "fallback": "Resumen de texto obligatorio de los archivos adjuntos que muestran aquellos clientes que entienden los adjuntos pero deciden no mostrarlos.",

            "text": f"Buenos dias! @{channel}",
            "pretext": f"Buenos dias! @{channel}",

            "color": "#36a64f",
            "fields": [
                {
                    "title": f"Opcion 1",
                    "value": "Sopa <https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx|Haz clic aquí> para obtener más detalles",
                    "short": False
                },
                {
                    "title": f"Opcion 3",
                    "value": "Lentejas <https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx|Haz clic aquí> para obtener más detalles",
                    "short": False
                },
                {
                    "title": f"Opcion 3",
                    "value": "Arroz <https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx|Haz clic aquí> para obtener más detalles",
                    "short": False
                }
            ]

        }
        # payload = {'Token':'My_Secret_Token','product':request.POST.get("options"),'price':request.POST.get("price")}
        r = requests.post(url, data=json.dumps(payload))

        if r.status_code == 200:
            data = r.json()
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
        return Response({"error": "Request failed"}, status=r.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
