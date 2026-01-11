import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def verify_auth():
    print("Iniciando pruebas de autenticación...")

    # 1. Registrar usuario
    print("\n[1] Registrando usuario de prueba...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "role": "admin"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print(f"✅ Registro exitoso: {response.json()}")
        elif response.status_code == 400 and "ya existe" in response.text:
             print(f"⚠️ Usuario ya existe (esto es esperado si corres la prueba varias veces)")
        else:
            print(f"❌ Error en registro: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. Asegúrate de que Flask esté corriendo.")
        return

    # 2. Login
    print("\n[2] Intentando iniciar sesión...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    token = None
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"✅ Login exitoso. Token recibido.")
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return

    # 3. Obtener perfil (/me)
    if token:
        print("\n[3] Obteniendo perfil de usuario (/me)...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Perfil obtenido correctamente: {response.json()}")
        else:
            print(f"❌ Error al obtener perfil: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Esperamos un momento por si el servidor se está reiniciando
    time.sleep(2)
    verify_auth()
