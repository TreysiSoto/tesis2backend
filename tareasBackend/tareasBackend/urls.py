from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from tareasAPI import views
from rest_framework import routers  # type: ignore
from django.contrib.auth import views as auth_views
router = routers.DefaultRouter()
router.register(r'registros', views.RegistroViewSet) 
router.register(r'trabajadores', views.TrabajadorViewSet)
router.register(r'empleadores', views.EmpleadorViewSet)
router.register(r'opiniones', views.OpinionViewSet)
router.register(r'notificaciones', views.NotificacionViewSet)
router.register(r'publicaciones', views.PublicacionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Incluye todas las rutas registradas en el router
    path('login/', views.LoginView.as_view(), name='login'),  # Mantén solo el login manualmente
    path('registro/', views.RegistroViewSet.as_view({'post': 'create'}), name='registro'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

