import google.generativeai as genai
from django.conf import settings
from datetime import datetime
import json

class IAService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Usar gemini-2.5-flash que es el más nuevo y rápido
            try:
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
                print(f"Modelo Gemini 2.5 Flash cargado exitosamente")
            except Exception as e:
                print(f"Error cargando modelo: {e}")
                self.model = None
        else:
            self.model = None
            print("GEMINI_API_KEY no configurada")
    
    def generar_json_mock(self, nombre_victima: str, clasificacion: str) -> dict:
        """
        Genera un JSON de respuesta simulado para testing sin IA
        """
        return {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "anonymous": True,
            "channel": "api",
            "reporter": {
                "relationship_to_company": "employee",
                "country": "México"
            },
            "people": {
                "offender": {
                    "name": nombre_victima,
                    "position": "Empleado",
                    "department": "General"
                }
            },
            "incident": {
                "type": clasificacion,
                "description": f"Denuncia de tipo {clasificacion} contra {nombre_victima}. Análisis generado en modo de prueba sin IA.",
                "approximate_date": datetime.now().strftime("%Y-%m"),
                "is_ongoing": True
            },
            "location": {
                "city": "Ciudad de México",
                "work_related": True
            },
            "evidence": {
                "has_evidence": False,
                "description": ""
            },
            "ai_analysis": "Este es un análisis generado en modo de prueba. Para obtener un análisis real, configure la GEMINI_API_KEY.",
            "status": "received",
            "case_id": f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
    
    def generar_json_con_ia(self, nombre_victima: str, clasificacion: str) -> dict:
        """
        Genera el JSON estructurado usando Gemini AI
        Aquí es donde puedes personalizar el prompt para que la IA genere los campos
        """
        
        # PROMPT PARA LA IA - Personaliza según necesites
        prompt = f"""Genera un reporte de denuncia en formato JSON válido.

Datos recibidos:
- Nombre de la víctima: {nombre_victima}
- Tipo de incidente: {clasificacion}

Debes generar un JSON con esta estructura EXACTA. IMPORTANTE: Responde SOLO con el JSON, sin texto antes o después, sin markdown:

{{
  "date": "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
  "anonymous": true,
  "channel": "web",
  "reporter": {{
    "relationship_to_company": "employee",
    "country": "México"
  }},
  "people": {{
    "offender": {{
      "name": "{nombre_victima}",
      "position": "Gerente",
      "department": "Administración"
    }}
  }},
  "incident": {{
    "type": "{clasificacion}",
    "description": "Descripción detallada del incidente de tipo {clasificacion}. Incluye contexto y detalles específicos en 2-3 oraciones.",
    "approximate_date": "{datetime.now().strftime('%Y-%m')}",
    "is_ongoing": true
  }},
  "location": {{
    "city": "Ciudad de México",
    "work_related": true
  }},
  "evidence": {{
    "has_evidence": true,
    "description": "Documentos y testimonios disponibles"
  }}
}}

Genera el JSON siguiendo esa estructura. Personaliza la descripción del incidente, el puesto y departamento de forma realista según el tipo de incidente."""

        if not self.model:
            print("Modelo no disponible, usando mock")
            return self.generar_json_mock(nombre_victima, clasificacion)

        try:
            print(f"Generando respuesta con IA para: {nombre_victima} - {clasificacion}")
            response = self.model.generate_content(prompt)
            respuesta_texto = response.text
            print(f"Respuesta recibida de IA ({len(respuesta_texto)} caracteres)")
            
            # Limpiar la respuesta por si tiene markdown
            respuesta_limpia = respuesta_texto.strip()
            if respuesta_limpia.startswith("```json"):
                respuesta_limpia = respuesta_limpia[7:]
            if respuesta_limpia.startswith("```"):
                respuesta_limpia = respuesta_limpia[3:]
            if respuesta_limpia.endswith("```"):
                respuesta_limpia = respuesta_limpia[:-3]
            respuesta_limpia = respuesta_limpia.strip()
            
            print(f"Respuesta limpia: {respuesta_limpia[:100]}...")
            
            # Parsear el JSON
            try:
                denuncia_json = json.loads(respuesta_limpia)
                print("JSON parseado exitosamente")
                
                return denuncia_json
                
            except json.JSONDecodeError as e:
                print(f"Error parseando JSON: {e}")
                print(f"Contenido problemático: {respuesta_limpia}")
                # Si falla el parseo, retornar mock
                return self.generar_json_mock(nombre_victima, clasificacion)
            
        except Exception as e:
            print(f"Error en IA: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self.generar_json_mock(nombre_victima, clasificacion)
    
    def procesar_denuncia(self, nombre_victima: str, clasificacion: str) -> str:
        """
        Método legacy para mantener compatibilidad con endpoint simple
        """
        prompt = f"""Eres un asistente legal especializado en denuncias. 
        
Se ha recibido una denuncia con los siguientes datos:
- Nombre de la víctima: {nombre_victima}
- Clasificación de la denuncia: {clasificacion}

Por favor, genera:
1. Un análisis preliminar de la situación
2. Recomendaciones de pasos a seguir
3. Información sobre los derechos de la víctima
4. Recursos disponibles para este tipo de casos

Responde de manera profesional, empática y orientada a ayudar."""

        if not self.model:
            return f"Análisis de denuncia - Víctima: {nombre_victima}, Tipo: {clasificacion}. Configure GEMINI_API_KEY para análisis completo."

        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error al procesar la solicitud con IA: {str(e)}"