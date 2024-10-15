from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from tareasAPI import views
from rest_framework import routers  # type: ignore

router = routers.DefaultRouter()
router.register(r'roles', views.RolViewSet)
router.register(r'registro', views.RegistroViewSet)  # Esto maneja automáticamente las rutas para RegistroViewSet
router.register(r'trabajadores', views.TrabajadorViewSet)
router.register(r'empleadores', views.EmpleadorViewSet)
router.register(r'opiniones', views.OpinionViewSet)
router.register(r'notificaciones', views.NotificacionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Incluye todas las rutas registradas en el router
    path('login/', views.LoginView.as_view(), name='login'),  # Mantén solo el login manualmente
]

