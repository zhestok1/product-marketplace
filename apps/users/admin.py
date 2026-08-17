from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Финансы', {'fields': ('balance',)}),
        ('Дополнительная информация', {'fields': ('avatar',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация',  {'fields': ('avatar',)}),
    )

    list_display = UserAdmin.list_display + ('balance', )
    list_filter = UserAdmin.list_filter
    list_editable = UserAdmin.list_editable + ()
    search_fields = UserAdmin.search_fields
    readonly_fields = ('balance', )