from flask import Blueprint, request, jsonify
from app import db
from app.models import Service, WorkOrder, OrderItem, User, Vehicle
from flask_jwt_extended import jwt_required, get_jwt_identity

# Creamos el Blueprint. Usaremos prefijo vacío para definir rutas absolutas como /services y /orders
# O mejor, un prefijo base '/api' si quisiéramos, pero seguiremos el patrón de auth/clients
orders_bp = Blueprint('orders', __name__)

# ==============================================================================
# Endpoint: Crear Servicio (Solo Admin)
# ==============================================================================
@orders_bp.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    """
    Crea un nuevo tipo de servicio en el catálogo.
    Solo permitido para usuarios con rol 'admin' o 'mecanico' (aunque el requerimiento dice admin).
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Verificación de rol (asumiendo que solo admin puede crear servicios)
    if not user or user.role != 'admin':
        return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403

    data = request.get_json()
    if not data or not data.get('name') or not data.get('base_price'):
        return jsonify({"msg": "Faltan datos obligatorios (name, base_price)"}), 400

    new_service = Service(
        name=data['name'],
        description=data.get('description', ''),
        base_price=float(data['base_price'])
    )

    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"msg": "Servicio creado exitosamente", "service": new_service.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear servicio: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Listar Servicios (Helper)
# ==============================================================================
@orders_bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services]), 200

# ==============================================================================
# Endpoint: Crear Orden de Trabajo
# ==============================================================================
@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """
    Crea una nueva orden de trabajo vinculada a un vehículo.
    El usuario creador se toma del token JWT.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('vehicle_id'):
        return jsonify({"msg": "Se requiere vehicle_id"}), 400
    
    # Validar existencia del vehículo
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({"msg": "Vehículo no encontrado"}), 404

    new_order = WorkOrder(
        vehicle_id=data['vehicle_id'],
        user_id=current_user_id,
        status='pendiente',
        total=0.0
    )

    try:
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"msg": "Orden creada exitosamente", "order": new_order.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear orden: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Agregar Item a Orden
# ==============================================================================
@orders_bp.route('/orders/<int:order_id>/items', methods=['POST'])
@jwt_required()
def add_order_item(order_id):
    """
    Agrega un servicio a una orden existente.
    Congela el precio del servicio en el momento de la agregación.
    Actualiza el total de la orden.
    """
    data = request.get_json()
    if not data or not data.get('service_id'):
        return jsonify({"msg": "Se requiere service_id"}), 400

    order = WorkOrder.query.get(order_id)
    if not order:
        return jsonify({"msg": "Orden no encontrada"}), 404

    service = Service.query.get(data['service_id'])
    if not service:
        return jsonify({"msg": "Servicio no encontrado"}), 404

    # Crear el item de la orden
    new_item = OrderItem(
        work_order_id=order_id,
        service_id=service.id,
        price_at_moment=service.base_price
    )

    try:
        db.session.add(new_item)
        
        # Actualizar el total de la orden
        order.total += service.base_price
        
        db.session.commit()
        return jsonify({"msg": "Servicio agregado a la orden", "item": new_item.to_dict(), "order_total": order.total}), 201
    except Exception as e:
        db.session.rollback()
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
    order = WorkOrder.query.get(order_id)
    if not order:
        return jsonify({"msg": "Orden no encontrada"}), 404
    
    # El método to_dict() del modelo WorkOrder ya debería incluir la anidación necesaria,
    # pero podemos enriquecerla aquí si es necesario.
    # Por ahora confiamos en el to_dict() que definimos en models.py
    
    response = order.to_dict()
    
    # Agregar info extra del vehículo/cliente si no estuviera ya (El modelo Vehicle tiene la FK pero la relación backref está en Client)
    # WorkOrder -> Vehicle -> Client
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

    new_status = data['status']
    valid_statuses = ['pendiente', 'en_progreso', 'finalizado', 'entregado']
    
    if new_status not in valid_statuses:
        return jsonify({"msg": f"Estado inválido. Permitidos: {', '.join(valid_statuses)}"}), 400

    order = WorkOrder.query.get(order_id)
    if not order:
        return jsonify({"msg": "Orden no encontrada"}), 404

    try:
        order.status = new_status
        db.session.commit()
        return jsonify({"msg": "Estado actualizado", "status": order.status}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al actualizar estado: {str(e)}"}), 500
