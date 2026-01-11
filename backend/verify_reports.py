import requests
import time
import random

BASE_URL = "http://127.0.0.1:5000"

def verify_reports():
    print("Iniciando pruebas de Reportes...")
    
    unique_suffix = random.randint(1000, 9999)

    # 1. Login como Admin
    print("\n[1] Autenticando como Admin...")
    admin_data = {
        "username": f"adminRep{unique_suffix}",
        "email": f"adminRep{unique_suffix}@example.com",
        "password": "securepass",
        "role": "admin"
    }
    # Registro
    requests.post(f"{BASE_URL}/auth/register", json=admin_data)
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": admin_data['email'], "password": admin_data['password']})
    if response.status_code != 200:
        print("❌ Error en login de admin")
        return
    token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login Admin exitoso.")

    # 2. Consultar Dashboard
    print("\n[2] Consultando Dashboard...")
    response = requests.get(f"{BASE_URL}/reports/dashboard", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Dashboard obtenido:")
        print(f"   - Total Órdenes (Mes): {data['total_orders_month']}")
        print(f"   - Ingreso Estimado (Finalizados): {data['estimated_income']}")
        print(f"   - Órdenes por Estado: {data['orders_by_status']}")
    else:
        print(f"❌ Error al consultar dashboard: {response.text}")

    # 3. Validar Seguridad (Intentar como usuario normal)
    print("\n[3] Probando acceso no autorizado (Usuario normal)...")
    # Registrar usuario normal
    user_data = {
        "username": f"userRep{unique_suffix}",
        "email": f"userRep{unique_suffix}@example.com",
        "password": "password",
        "role": "recepcion"
    }
    requests.post(f"{BASE_URL}/auth/register", json=user_data)
    user_login = requests.post(f"{BASE_URL}/auth/login", json={"email": user_data['email'], "password": "password"})
    user_token = user_login.json()['access_token']
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    response = requests.get(f"{BASE_URL}/reports/dashboard", headers=user_headers)
    if response.status_code == 403:
        print(f"✅ Acceso denegado correctamente para usuario no-admin (403 Forbidden)")
    else:
        print(f"⚠️ Alerta: Usuario normal pudo acceder o error inesperado: {response.status_code}")

if __name__ == "__main__":
    time.sleep(1)
    verify_reports()
