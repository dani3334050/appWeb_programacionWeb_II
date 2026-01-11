import requests
import random
import time

BASE_URL = "http://127.0.0.1:5000"

def verify_orders_workflow():
    print("Iniciando pruebas de Órdenes y Servicios...")
    
    unique_suffix = random.randint(1000, 9999)
    
    # 1. Crear Usuario Admin y Login (para poder crear Servicios)
    print("\n[1] Autenticando como Admin...")
    admin_data = {
        "username": f"admin{unique_suffix}",
        "email": f"admin{unique_suffix}@example.com",
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

    # 2. Crear Servicio (Requiere Token Admin)
    print("\n[2] Creando Servicio 'Afinación Completa'...")
    service_data = {
        "name": "Afinación Completa",
        "description": "Cambio de bujías, filtros y aceite",
        "base_price": 450.50
    }
    response = requests.post(f"{BASE_URL}/services", json=service_data, headers=headers)
    if response.status_code == 201:
        service = response.json().get('service')
        service_id = service['id']
        print(f"✅ Servicio creado: {service['name']} (ID: {service_id}) - Precio: {service['base_price']}")
    else:
        print(f"❌ Error al crear servicio: {response.text}")
        return

    # 3. Preparar Datos: Cliente y Vehículo
    print("\n[3] Preparando Cliente y Vehículo...")
    client_res = requests.post(f"{BASE_URL}/clients", json={
        "first_name": "ClienteOrden", "last_name": "Test", "email": f"cliente{unique_suffix}@test.com"
    })
    client_id = client_res.json()['client']['id']
    
    vehicle_res = requests.post(f"{BASE_URL}/clients/{client_id}/vehicles", json={
        "plate": f"ORD-{unique_suffix}", "brand": "Nissan", "model": "Sentra", "year": 2022
    })
    vehicle_id = vehicle_res.json()['vehicle']['id']
    print(f"✅ Vehículo listo: Nissan Sentra (ID: {vehicle_id})")

    # 4. Crear Orden de Trabajo
    print("\n[4] Creando Orden de Trabajo...")
    order_data = {"vehicle_id": vehicle_id}
    response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
    if response.status_code == 201:
        order = response.json().get('order')
        order_id = order['id']
        print(f"✅ Orden creada (ID: {order_id}) - Estado: {order['status']}")
    else:
        print(f"❌ Error al crear orden: {response.text}")
        return

    # 5. Agregar Item a la Orden
    print("\n[5] Agregando Servicio a la Orden...")
    item_data = {"service_id": service_id}
    response = requests.post(f"{BASE_URL}/orders/{order_id}/items", json=item_data, headers=headers)
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Item agregado. Nuevo Total Orden: {data['order_total']}")
    else:
        print(f"❌ Error al agregar item: {response.text}")

    # 6. Consultar Detalle Completo
    print("\n[6] Consultando detalle completo de la Orden...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        full_order = response.json()
        print(f"✅ Detalle obtenido. Vehículo: {full_order.get('vehicle_info', {}).get('plate')}")
        print(f"✅ Items en la orden: {len(full_order.get('items', []))}")
    else:
        print(f"❌ Error al consultar orden: {response.text}")

    # 7. Actualizar Estado
    print("\n[7] Actualizando estado a 'en_progreso'...")
    response = requests.put(f"{BASE_URL}/orders/{order_id}/status", json={"status": "en_progreso"}, headers=headers)
    if response.status_code == 200:
        print(f"✅ Estado actualizado: {response.json()['status']}")
    else:
        print(f"❌ Error al actualizar estado: {response.text}")

if __name__ == "__main__":
    time.sleep(1)
    verify_orders_workflow()
