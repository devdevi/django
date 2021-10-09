"""Menu URLs"""

# Django
from django.urls import path

# views
from backend_test.menus.views import crear_plato

urlpatterns = [
    path('platos/', crear_plato)
]
