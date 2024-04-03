from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mahsulot, CustomUser


@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kategoriya', 'qadoq',
                    'quti', 'massa', 'miqdori', 'kelgan_sana', 'tavsifi')
    search_fields = ('nomi', 'kategoriya', 'kelgan_sana')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add 'is_manager' to the list display
    list_display = ['username', 'email', 'is_staff', 'is_manager']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
         'user_permissions', 'is_manager')}),  # Add 'is_manager' to the permissions fieldset
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
