from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# models
from backend_test.users.models import User, Employee

class CustomUserAdmin(UserAdmin):

    list_display =  ('username', 'email', 'is_employed', 'is_admin')
    list_filter = ('is_employed',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display =  ('user', 'biography')
    list_filter = ('menus', 'menus_taken',)


admin.site.register(User, CustomUserAdmin)
