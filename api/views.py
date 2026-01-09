from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from datetime import datetime
from .models import Denuncia
from .serializers import UserSerializer, DenunciaSerializer, DenunciaCreateSerializer
from .services import IAService

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Endpoint para registrar nuevos usuarios
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Usuario creado exitosamente',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def procesar_denuncia(request):
    """
    Endpoint protegido que recibe víctima y clasificación
    La IA genera el JSON completo estructurado
    """
    try:
        print("=" * 60)
        print("INICIO DE PROCESAR_DENUNCIA")
        print("=" * 60)
        
        serializer = DenunciaCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Validación fallida: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        nombre_victima = serializer.validated_data['nombre_victima']
        clasificacion = serializer.validated_data['clasificacion']
        print(f"Datos validados: {nombre_victima} - {clasificacion}")
        
        # Generar JSON estructurado con IA
        print("Iniciando generación con IA...")
        ia_service = IAService()
        denuncia_json = ia_service.generar_json_con_ia(nombre_victima, clasificacion)
        print(f"JSON generado: {type(denuncia_json)}")
        print(f"Claves del JSON: {denuncia_json.keys()}")
        
        # Guardar en base de datos
        print("Guardando en base de datos...")
        print(f"Usuario: {request.user}")
        print(f"Nombre víctima: {nombre_victima}")
        print(f"Clasificación: {clasificacion}")
        print(f"AI Analysis: {denuncia_json.get('ai_analysis', 'N/A')[:50]}...")
        
        denuncia = Denuncia.objects.create(
            usuario=request.user,
            nombre_victima=nombre_victima,
            clasificacion=clasificacion,
            respuesta_ia=denuncia_json.get('ai_analysis', ''),
            datos_completos=denuncia_json
        )
        print(f"Denuncia guardada con ID: {denuncia.id}")
        print("=" * 60)
        return Response(denuncia_json, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Log del error completo
        import traceback
        print("=" * 60)
        print("ERROR EN PROCESAR_DENUNCIA:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("\nTraceback completo:")
        print(traceback.format_exc())
        print("=" * 60)
        
        return Response({
            'error': str(e),
            'type': type(e).__name__,
            'detail': 'Error al procesar la denuncia. Revisa los logs del servidor.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def procesar_denuncia_mock(request):
    """
    Endpoint de prueba para testing sin API key de Anthropic
    Genera el JSON estructurado sin usar IA real
    """
    try:
        serializer = DenunciaCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        nombre_victima = serializer.validated_data['nombre_victima']
        clasificacion = serializer.validated_data['clasificacion']
        
        # Generar JSON mock (sin IA)
        ia_service = IAService()
        denuncia_json = ia_service.generar_json_mock(nombre_victima, clasificacion)
        
        # Guardar en base de datos
        denuncia = Denuncia.objects.create(
            usuario=request.user,
            nombre_victima=nombre_victima,
            clasificacion=clasificacion,
            respuesta_ia=denuncia_json.get('ai_analysis', ''),
            datos_completos=denuncia_json
        )
        
        # Agregar el ID de la base de datos al JSON
        denuncia_json['id'] = denuncia.id
        
        return Response(denuncia_json, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Log del error completo
        import traceback
        print("=" * 50)
        print("ERROR EN PROCESAR_DENUNCIA_MOCK:")
        print(traceback.format_exc())
        print("=" * 50)
        
        return Response({
            'error': str(e),
            'detail': 'Error al procesar la denuncia mock. Revisa los logs del servidor.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_denuncias(request):
    """
    Endpoint para obtener las denuncias del usuario autenticado
    """
    denuncias = Denuncia.objects.filter(usuario=request.user)
    serializer = DenunciaSerializer(denuncias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    """
    Endpoint para obtener información del usuario autenticado
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_auth(request):
    """
    Endpoint de prueba para verificar autenticación
    """
    return Response({
        'message': 'Autenticación exitosa',
        'user': request.user.username,
        'is_authenticated': request.user.is_authenticated
    })