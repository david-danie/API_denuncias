from django.db import models
from django.contrib.auth.models import User

class Denuncia(models.Model):
    CLASIFICACIONES = [
        ('robo', 'Robo'),
        ('violencia', 'Violencia'),
        ('fraude', 'Fraude'),
        ('fraud', 'Fraud'),
        ('acoso', 'Acoso'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denuncias')
    nombre_victima = models.CharField(max_length=255)
    clasificacion = models.CharField(max_length=50, choices=CLASIFICACIONES)
    respuesta_ia = models.TextField(blank=True, null=True)
    datos_completos = models.JSONField(blank=True, null=True, default=dict)  # Agregar default
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Denuncia'
        verbose_name_plural = 'Denuncias'
    
    def __str__(self):
        return f"Denuncia de {self.nombre_victima} - {self.clasificacion}"