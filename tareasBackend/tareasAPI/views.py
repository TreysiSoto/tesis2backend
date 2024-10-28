from rest_framework import viewsets, status, generics  # type: ignore
from django.contrib.auth import authenticate, login  # type: ignore
from rest_framework.response import Response  # type: ignore
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework.decorators import api_view # type: ignore
from . import models
from . import serializers
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Si usas CSRF, elimina esta línea y agrega el token en el header
class PasswordResetConfirmView(View):
    def post(self, request):
        data = json.loads(request.body)
        uidb64 = data.get('uidb64')
        token = data.get('token')
        new_password = data.get('new_password')

        try:
            # Decodificar uidb64 para obtener el ID del usuario
            uid = urlsafe_base64_decode(uidb64).decode()
            usuario = models.Usuario.objects.get(pk=uid)

            # Verificar el token
            if default_token_generator.check_token(usuario, token):
                usuario.set_password(new_password)
                usuario.save()
                return JsonResponse({'message': _('Password has been reset successfully.')}, status=200)
            else:
                return JsonResponse({'error': _('Token is invalid.')}, status=400)
        except (TypeError, ValueError, OverflowError, models.Usuario.DoesNotExist):
            return JsonResponse({'error': _('Invalid UID.')}, status=400)

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        correo = request.data.get('correo')
        password = request.data.get('password')

        # Autenticar al usuario
        usuario = authenticate(correo=correo, password=password)
        
        if usuario is not None:
            # Asegúrate de que usuario es una instancia de Usuario
            if isinstance(usuario, models.Usuario):
                rol_nombre = usuario.rol  # Accede a rol directamente como un atributo
                if rol_nombre == 'trabajador':
                    return Response({"mensaje": "Inicio de sesión exitoso", "rol": rol_nombre, "perfil": "trabajador"}, status=status.HTTP_200_OK)
                elif rol_nombre == 'empleador':
                    return Response({"mensaje": "Inicio de sesión exitoso", "rol": rol_nombre, "perfil": "empleador"}, status=status.HTTP_200_OK)
        else:
            return Response({"mensaje": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer

    def create(self, request, *args, **kwargs):
        # Obtener el rol del request
        rol_nombre = request.data.get('rol') 

        # Convertir request.data a un diccionario normal
        usuario_data = request.data.copy()  # Esto crea una copia mutable

        # Asignar el nombre del rol directamente
        usuario_data['rol'] = rol_nombre  # Ahora rol es un CharField, así que solo se guarda el nombre

        serializer = self.get_serializer(data=usuario_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({"mensaje": "Registro exitoso", "rol": rol_nombre}, status=status.HTTP_201_CREATED)

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = models.Trabajador.objects.all()
    serializer_class = serializers.TrabajadorSerializer

class EmpleadorViewSet(viewsets.ModelViewSet):
    queryset = models.Empleador.objects.all()
    serializer_class = serializers.EmpleadorSerializer

class OpinionViewSet(viewsets.ModelViewSet):
    queryset = models.Opinion.objects.all()
    serializer_class = serializers.OpinionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = models.Notificacion.objects.all()
    serializer_class = serializers.NotificacionSerializer

class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = models.Publicacion.objects.all()
    serializer_class = serializers.PublicacionSerializer

    # Sobrescribir para asignar automáticamente el empleador al crear la publicación
    def perform_create(self, serializer):
        empleador = self.request.user.empleador  # Asignar el empleador basado en el usuario autenticado
        serializer.save(empleador=empleador)

class FeedView(generics.ListAPIView):
    queryset = models.Publicacion.objects.all()
    serializer_class = serializers.PublicacionSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.rol == 'empleador':  # Accede al rol directamente
            return models.Publicacion.objects.filter(empleador=usuario)
        return models.Publicacion.objects.none()  # Mostrar solo las publicaciones del empleador
