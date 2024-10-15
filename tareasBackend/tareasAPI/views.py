from rest_framework import viewsets,status, generics # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from . import models
from . import serializers


class RolViewSet(viewsets.ModelViewSet):
    queryset = models.Rol.objects.all()
    serializer_class = serializers.RolSerializer
    
class RegistroViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

class LoginView(generics.GenericAPIView):
    def post(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')
        usuario = authenticate(correo=correo, password=password)
        if usuario is not None:
            # Aquí puedes generar un token si usas autenticación basada en tokens
            return Response({"mensaje": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
        return Response({"mensaje": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

