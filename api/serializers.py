from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Denuncia

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class DenunciaSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    
    class Meta:
        model = Denuncia
        fields = ('id', 'usuario', 'nombre_victima', 'clasificacion', 'respuesta_ia', 'fecha_creacion')
        read_only_fields = ('respuesta_ia', 'fecha_creacion')

class DenunciaCreateSerializer(serializers.Serializer):
    nombre_victima = serializers.CharField(max_length=255)
    clasificacion = serializers.ChoiceField(choices=Denuncia.CLASIFICACIONES)