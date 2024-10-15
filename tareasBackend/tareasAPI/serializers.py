from rest_framework import serializers # type: ignore
from . import models
from django.contrib.auth.hashers import make_password  # type: ignore # Importa make_password

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = ['id', 'nombre']  # Incluye el campo 'id' si lo necesitas
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['correo', 'nombre', 'rol', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        usuario = models.Usuario(
            correo=validated_data['correo'],
            nombre=validated_data['nombre'],
            rol=validated_data['rol']
        )
        usuario.set_password(validated_data['password'])  # Hashea la contraseña
        usuario.save()
        return usuario

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trabajador
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'dni', 
                  'direccion', 'telefono', 'trabajo', 'antecedentes_policiales', 'usuario']

class EmpleadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Empleador
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'dni', 
                  'direccion', 'telefono', 'antecedentes_policiales', 'usuario']

class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Opinion
        fields = ['id', 'calificacion', 'comentario', 'fecha', 
                  'empleador', 'trabajador']  # Incluye el ID del empleador y trabajador

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notificacion
        fields = ['id', 'mensaje', 'fecha']