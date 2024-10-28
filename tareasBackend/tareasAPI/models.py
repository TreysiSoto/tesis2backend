from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo electrónico es obligatorio")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)  # Asegúrate de que la contraseña esté hasheada
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    ROL_CHOICES = [
        ('trabajador', 'Trabajador'),
        ('empleador', 'Empleador'),
    ]
    rol = models.CharField(max_length=50, choices=ROL_CHOICES)  # Campo de rol como CharField
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'  # Campo único para el inicio de sesión
    REQUIRED_FIELDS = ['nombre', 'rol']  # Campos adicionales obligatorios

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} - {self.rol}" # Muestra el nombre y rol en el string

class Trabajador(models.Model):
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=180)
    apellido_materno = models.CharField(max_length=180)
    dni = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=255, null=False, blank=True)
    telefono = models.CharField(max_length=20, null=False, blank=True)
    trabajo = models.CharField(max_length=100)
    antecedentes_policiales = models.CharField(max_length=255, null=False, blank=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} - DNI: {self.dni}"

class Empleador(models.Model):
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=180)
    apellido_materno = models.CharField(max_length=180)
    dni = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255, null=False, blank=True)
    telefono = models.CharField(max_length=20, null=False, blank=True)
    antecedentes_policiales = models.CharField(max_length=255, null=False, blank=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} - DNI: {self.dni}"

class Opinion(models.Model):
    calificacion = models.FloatField()  
    comentario = models.TextField()  
    fecha = models.DateField(auto_now_add=True)  
    empleador = models.ForeignKey(Empleador, on_delete=models.CASCADE)  
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Calificación: {self.calificacion} - Fecha: {self.fecha}"
    
class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje: {self.mensaje[:20]}... - Fecha: {self.fecha}"

class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)  # Breve título del trabajo
    descripcion = models.TextField()  # Descripción del trabajo
    ubicacion = models.CharField(max_length=255)  # Dirección donde se realizará el trabajo
    fecha_limite = models.DateField()  # Fecha límite para realizar el trabajo
    empleador = models.ForeignKey(Empleador, on_delete=models.CASCADE)  # Empleador que crea la publicación
    fecha_publicacion = models.DateField(auto_now_add=True)  # Fecha en la que se creó la publicación

    def __str__(self):
        return f"{self.titulo} - {self.empleador.nombre}"
