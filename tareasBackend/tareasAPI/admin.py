from django.contrib import admin

# Register your models here.

#Username (leave blank to use 'hp'): trey29
#Email address: trey@gmail.com
#contra: enf.........

from .models import Rol, Usuario, Trabajador, Empleador, Opinion, Notificacion

# Registrar los modelos en el panel de administración
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Trabajador)
admin.site.register(Empleador)
admin.site.register(Opinion)
admin.site.register(Notificacion)