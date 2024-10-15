from django.contrib.auth.backends import BaseBackend
from .models import Usuario

from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class CorreoAuthBackend(BaseBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        # Verifica que se haya proporcionado un correo y una contraseña
        if correo is None or password is None:
            return None
        
        try:
            # Intenta obtener el usuario por correo electrónico
            user = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return None
        
        # Verifica la contraseña
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
