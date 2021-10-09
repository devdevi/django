from django.contrib import admin

# models
from backend_test.menus.models import Menu, Plato


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha', 'activo')
    list_filter = ('activo',)


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'observaciones')
