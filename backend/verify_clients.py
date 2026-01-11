import requests
import time
import random

BASE_URL = "http://127.0.0.1:5000"

def verify_clients_vehicles():
    print("Iniciando pruebas de Clientes y Vehículos...")

    # 1. Crear Cliente
    print("\n[1] Creando un nuevo cliente...")
    # Usamos un email aleatorio para evitar conflictos si corremos el script varias veces
    random_id = random.randint(1000, 9999)
    client_data = {
        "first_name": "Juan",
        "last_name": "Perez",
        "email": f"juan.perez{random_id}@example.com",
        "phone": "555-0123",
        "address": "Calle Falsa 123"
    }
    
    client_id = None
    try:
        response = requests.post(f"{BASE_URL}/clients", json=client_data)
        if response.status_code == 201:
            client = response.json().get('client')
            client_id = client.get('id')
            print(f"✅ Cliente creado: {client}")
        else:
            print(f"❌ Error al crear cliente: {response.status_code} - {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        return

    # 2. Listar Clientes
    print("\n[2] Listando todos los clientes...")
    response = requests.get(f"{BASE_URL}/clients")
    if response.status_code == 200:
        clients = response.json()
        print(f"✅ Clientes encontrados: {len(clients)}")
    else:
        print(f"❌ Error al listar clientes: {response.status_code} - {response.text}")

    # 3. Agregar Vehículo al Cliente
    if client_id:
        print(f"\n[3] Agregando vehículo al cliente ID {client_id}...")
        vehicle_data = {
            "plate": f"ABC-{random_id}",
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "vin": f"VIN{random_id}XYZ"
        }
        
        response = requests.post(f"{BASE_URL}/clients/{client_id}/vehicles", json=vehicle_data)
        if response.status_code == 201:
            vehicle = response.json().get('vehicle')
            print(f"✅ Vehículo agregado: {vehicle}")
        else:
            print(f"❌ Error al agregar vehículo: {response.status_code} - {response.text}")

        # 4. Listar Vehículos del Cliente
        print(f"\n[4] Listando vehículos del cliente ID {client_id}...")
        response = requests.get(f"{BASE_URL}/clients/{client_id}/vehicles")
        if response.status_code == 200:
            vehicles = response.json()
            print(f"✅ Vehículos encontrados para el cliente: {len(vehicles)}")
            print(vehicles)
        else:
            print(f"❌ Error al listar vehículos del cliente: {response.status_code} - {response.text}")

if __name__ == "__main__":
    time.sleep(1) # Esperar un poco
    verify_clients_vehicles()
