from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

# ==============================================================================
# Capa de RUTAS (Controlador) - Orders
# ==============================================================================
# Esta capa se encarga EXCLUSIVAMENTE de:
# 1. Recibir la petición HTTP (GET, POST, etc.)
# 2. Extraer y validar básicamente los datos de entrada (JSON, Params)
# 3. Llamar a la Capa de Servicios (OrderService) para ejecutar la lógica
# 4. Retornar la respuesta HTTP adecuada (JSON + Status Code)
# ==============================================================================

orders_bp = Blueprint('orders', __name__, url_prefix='/api')

# ==============================================================================
# Endpoint: Crear Servicio (Solo Admin)
# ==============================================================================
@orders_bp.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    """
    Crea un nuevo tipo de servicio en el catálogo.
    Endpoint protegido para administradores.

    Request Body:
        name (str): Nombre del servicio.
        base_price (float): Precio base.
        description (str): Descripción opcional.

    Returns:
        JSON: Objeto del servicio creado.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Verificación de rol (Controlador valida permisos HTTP)
    if not user or user.role != 'admin':
        return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403

    data = request.get_json()
    # Validación básica de entrada
    if not data or not data.get('name') or not data.get('base_price'):
        return jsonify({"msg": "Faltan datos obligatorios (name, base_price)"}), 400

    try:
        # Llamada al servicio para lógica de negocio
        new_service = OrderService.create_service(
            name=data['name'],
            base_price=float(data['base_price']),
            description=data.get('description', '')
        )
        return jsonify({"msg": "Servicio creado exitosamente", "service": new_service.to_dict()}), 201
    except Exception as e:
        return jsonify({"msg": f"Error al crear servicio: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Listar Servicios (Helper)
# ==============================================================================
@orders_bp.route('/services', methods=['GET'])
def get_services():
    """
    Obtiene la lista de todos los servicios disponibles.
    Público (o protegido según requerimiento, aquí público).
    """
    services = OrderService.get_all_services()
    return jsonify([s.to_dict() for s in services]), 200

# ==============================================================================
# Endpoint: Detalle de Servicio
# ==============================================================================
@orders_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = OrderService.get_service_by_id(service_id)
    if not service:
        return jsonify({"msg": "Servicio no encontrado"}), 404
    return jsonify(service.to_dict()), 200

# ==============================================================================
# Endpoint: Actualizar Servicio (Solo Admin)
# ==============================================================================
@orders_bp.route('/services/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403

    data = request.get_json() or {}
    try:
        updated = OrderService.update_service(
            service_id,
            name=data.get('name'),
            base_price=data.get('base_price'),
            description=data.get('description')
        )
        return jsonify({"msg": "Servicio actualizado", "service": updated.to_dict()}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error al actualizar servicio: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Eliminar Servicio (Solo Admin)
# ==============================================================================
@orders_bp.route('/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403
    try:
        OrderService.delete_service(service_id)
        return jsonify({"msg": "Servicio eliminado"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error al eliminar servicio: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Crear Orden de Trabajo
# ==============================================================================
@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """
    Crea una nueva orden de trabajo vinculada a un vehículo.
    Usuario autenticado es el creador.

    Request Body:
        vehicle_id (int): ID del vehículo.

    Returns:
        JSON: La orden creada.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('vehicle_id'):
        return jsonify({"msg": "Se requiere vehicle_id"}), 400
    
    try:
        # Delegamos al servicio
        new_order = OrderService.create_order(
            vehicle_id=data['vehicle_id'],
            user_id=current_user_id
        )
        return jsonify({"msg": "Orden creada exitosamente", "order": new_order.to_dict()}), 201
    except ValueError as e:
        # Capturamos excepciones de negocio específicas (ej: vehículo no encontrado)
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error al crear orden: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Listar Órdenes
# ==============================================================================
@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """
    Obtiene la lista de todas las órdenes de trabajo.
    """
    try:
        orders = OrderService.get_all_orders()
        response = []
        for order in orders:
             order_dict = order.to_dict()
             # Enriquecer con info básica de vehiculo para la tabla
             if order.vehicle:
                 order_dict['vehicle_plate'] = order.vehicle.plate
             response.append(order_dict)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"msg": f"Error al obtener órdenes: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Agregar Item a Orden
# ==============================================================================
@orders_bp.route('/orders/<int:order_id>/items', methods=['POST'])
@jwt_required()
def add_order_item(order_id):
    """
    Agrega un servicio a una orden existente.

    Path Params:
        order_id (int): ID de la orden.
    
    Request Body:
        service_id (int): ID del servicio a agregar.

    Returns:
        JSON: Item creado y nuevo total de la orden.
    """
    data = request.get_json()
    if not data or not data.get('service_id'):
        return jsonify({"msg": "Se requiere service_id"}), 400

    try:
        # Delegamos la lógica compleja (crear item + actualizar total orden) al servicio
        new_item, order_total = OrderService.add_order_item(
            order_id=order_id,
            service_id=data['service_id']
        )
        return jsonify({
            "msg": "Servicio agregado a la orden", 
            "item": new_item.to_dict(), 
            "order_total": order_total
        }), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error al agregar item: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Obtener Detalle de Orden
# ==============================================================================
@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    Obtiene el detalle completo de una orden: Cliente, Vehículo, Items.
    """
    order = OrderService.get_order_by_id(order_id)
    if not order:
        return jsonify({"msg": "Orden no encontrada"}), 404
    
    response = order.to_dict()
    
    # Enriquecimiento de respuesta para el Frontend (opcional pero útil)
    if order.vehicle:
          response['vehicle_info'] = order.vehicle.to_dict()
          if order.vehicle.owner:
              response['client_info'] = order.vehicle.owner.to_dict()

    return jsonify(response), 200

# ==============================================================================
# Endpoint: Actualizar Estado de Orden
# ==============================================================================
@orders_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """
    Actualiza el estado de la orden (pendiente, en_progreso, finalizado).
    """
    data = request.get_json()
    if not data or not data.get('status'):
        return jsonify({"msg": "Se requiere status"}), 400

    try:
        order = OrderService.update_order_status(order_id, data['status'])
        return jsonify({"msg": "Estado actualizado", "status": order.status}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error al actualizar estado: {str(e)}"}), 500
