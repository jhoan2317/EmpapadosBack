from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib.auth.models import User
        from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
        
        username_field = User._meta.get_field('username')
        
        # Nuevos validadores: solo letras, longitud 4-20
        username_field.validators = [
            RegexValidator(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$', 
                "El nombre de usuario solo puede contener letras."
            ),
            MinLengthValidator(4, "El nombre de usuario debe tener al menos 4 caracteres."),
            MaxLengthValidator(20, "El nombre de usuario no puede exceder los 20 caracteres.")
        ]
        
        # Actualizar el texto de ayuda que se ve en el Admin
        username_field.help_text = "Requerido. Entre 4 y 20 caracteres. Solo letras (sin números ni símbolos)."
        username_field.max_length = 20
