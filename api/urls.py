from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('test-auth/', views.test_auth, name='test_auth'),
    path('denuncia/', views.procesar_denuncia, name='procesar_denuncia'),
    path('denuncia-mock/', views.procesar_denuncia_mock, name='procesar_denuncia_mock'),
    path('mis-denuncias/', views.mis_denuncias, name='mis_denuncias'),
]