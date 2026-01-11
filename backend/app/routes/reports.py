from flask import Blueprint, jsonify
from app import db
from app.models import WorkOrder, OrderItem, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract
from datetime import datetime

# Creamos el Blueprint para los reportes
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# ==============================================================================
# Endpoint: Dashboard (Métricas)
# ==============================================================================
@reports_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_metrics():
    """
    Devuelve métricas clave para el panel de administración.
    Solo accesible para administradores.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Verificación de rol (Admin only)
    if not user or user.role != 'admin':
        return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403

    try:
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year

        # 1. Total de órdenes del mes actual
        total_orders_month = db.session.query(func.count(WorkOrder.id))\
            .filter(extract('month', WorkOrder.created_at) == current_month)\
            .filter(extract('year', WorkOrder.created_at) == current_year)\
            .scalar()

        # 2. Ingreso estimado (Suma de items de órdenes finalizadas)
        # Hacemos un JOIN entre OrderItem y WorkOrder para filtrar por el estado de la orden
        estimated_income = db.session.query(func.sum(OrderItem.price_at_moment))\
            .join(WorkOrder)\
            .filter(WorkOrder.status == 'finalizado')\
            .scalar()
        
        # Si no hay ventas, sum devuelve None, lo convertimos a 0
        if estimated_income is None:
            estimated_income = 0.0

        # 3. Conteo de órdenes por estado
        # Retorna una lista de tuplas: [('pendiente', 5), ('finalizado', 10), ...]
        orders_by_status_query = db.session.query(WorkOrder.status, func.count(WorkOrder.status))\
            .group_by(WorkOrder.status)\
            .all()
        
        # Convertimos la lista de tuplas a un diccionario para mejor uso en frontend
        orders_by_status = {status: count for status, count in orders_by_status_query}

        return jsonify({
            "total_orders_month": total_orders_month,
            "estimated_income": estimated_income,
            "orders_by_status": orders_by_status
        }), 200

    except Exception as e:
        return jsonify({"msg": f"Error al generar reporte: {str(e)}"}), 500
