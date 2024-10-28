from rest_framework import serializers  # type: ignore
from . import models
from django.contrib.auth.hashers import make_password  # type: ignore # Importa make_password

class UsuarioSerializer(serializers.ModelSerializer):
    # Definimos el campo 'rol' como un ChoiceField
    rol = serializers.ChoiceField(choices=models.Usuario.ROL_CHOICES)

    class Meta:
        model = models.Usuario
        fields = ['id', 'nombre', 'correo', 'password', 'rol']  # Incluir todos los campos necesarios
        extra_kwargs = {
            'password': {'write_only': True}  # Asegura que la contraseña solo se escriba
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extraemos la contraseña
        usuario = models.Usuario(**validated_data)  # Creamos el objeto Usuario
        usuario.set_password(password)  # Hasheamos la contraseña
        usuario.save()  # Guardamos el usuario
        return usuario  # Retornamos el usuario creado

    
class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

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

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publicacion
        fields = ['id', 'titulo', 'descripcion', 'ubicacion', 'fecha_limite', 
                  'empleador', 'fecha_publicacion']
