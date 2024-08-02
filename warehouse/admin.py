from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Mahsulot, CustomUser, Customer, ProductHistory
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission


@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kategoriya', 'qadoq',
                    'quti', 'massa', 'miqdori', 'kelgan_sana', 'tavsifi')
    search_fields = ('nomi', 'kategoriya', 'kelgan_sana')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number')
    search_fields = ('name', 'location', 'phone_number')


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'transaction_type', 'quantity')
    search_fields = ('product_id', 'transaction_type', 'quantity')


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # Add 'is_manager' to the list display
#     list_display = ['username', 'email',
#                     'is_staff', 'is_manager', 'name', 'photo']
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('email',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
#          'user_permissions', 'is_manager')}),  # Add 'is_manager' to the permissions fieldset
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )


# admin.site.register(CustomUser, CustomUserAdmin)

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'name', 'email', 'is_manager', 'photo')
    list_filter = ('is_manager',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'photo')}),
        ('Permissions', {
         'fields': ('is_manager', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'photo', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        # If the object is being created, set the default permissions or other custom logic
        if not change:
            # Example logic: Automatically set is_manager to False by default
            obj.is_manager = False
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
