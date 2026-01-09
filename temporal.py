import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ No se encontró GEMINI_API_KEY en .env")
    exit(1)

print(f"✅ API Key encontrada: {api_key[:20]}...")
genai.configure(api_key=api_key)

print("\n" + "="*60)
print("PROBANDO MODELO GEMINI 2.5 FLASH...")
print("="*60)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content("Di 'Hola' en una sola palabra")
    print(f"✅ Modelo funciona perfectamente!")
    print(f"Respuesta: {response.text}")
    
    print("\n" + "="*60)
    print("PROBANDO GENERACIÓN DE JSON...")
    print("="*60)
    
    prompt = """Genera un JSON simple con este formato:
{
  "nombre": "Juan",
  "edad": 30
}

Responde SOLO con el JSON, sin texto adicional."""
    
    response = model.generate_content(prompt)
    print(f"Respuesta JSON:\n{response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    
print("\n✅ Todo listo para usar en Django!")