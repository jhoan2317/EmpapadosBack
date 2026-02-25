from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# Unregister the original UserAdmin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    
    # Añadimos el email y el telefono a la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_telefono', 'is_staff')
    list_select_related = ('profile', )

    def get_telefono(self, instance):
        return instance.profile.telefono
    get_telefono.short_description = 'Teléfono'

    # Ensure profile is saved when user is saved in admin
    def save_model(self, request, obj, form, change):
        # Set a flag to tell the signal to ignore this instance creation
        # because the Admin Inline will handle it.
        if not change: # If it's a new user
            obj._ignore_profile_signal = True
        super().save_model(request, obj, form, change)
