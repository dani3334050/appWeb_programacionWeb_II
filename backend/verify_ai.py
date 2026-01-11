import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def verify_ai():
    print("Iniciando prueba de AI Endpoint...")

    # 1. Probar endpoint /ai/ask
    print("\n[1] Enviando pregunta a /ai/ask...")
    data = {
        "question": "¿Cúanto cuesta un cambio de aceite?",
        "context": "Historial de conversación..."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/ask", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta recibida: {result['response']}")
            print(f"✅ Echo de pregunta: {result['question_received']}")
        else:
            print(f"❌ Error en endpoint AI: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

if __name__ == "__main__":
    time.sleep(1)
    verify_ai()
