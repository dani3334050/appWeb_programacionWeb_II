from flask import Blueprint, request, jsonify
from app import db
from app.models import CarListing, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/api/marketplace')

# ==============================================================================
# Obtener todas las publicaciones (Feed Público)
# ==============================================================================
@marketplace_bp.route('/', methods=['GET'])
def get_listings():
    """
    Obtiene todas las publicaciones de autos disponibles.
    No requiere autenticación (Público).
    """
    listings = CarListing.query.filter_by(status='available').order_by(CarListing.created_at.desc()).all()
    return jsonify([listing.to_dict() for listing in listings]), 200

# ==============================================================================
# Obtener mis publicaciones (Cliente)
# ==============================================================================
@marketplace_bp.route('/my-listings', methods=['GET'])
@jwt_required()
def get_my_listings():
    """
    Obtiene las publicaciones del usuario autenticado.
    """
    current_user_id = get_jwt_identity()
    listings = CarListing.query.filter_by(user_id=current_user_id).order_by(CarListing.created_at.desc()).all()
    return jsonify([listing.to_dict() for listing in listings]), 200

# ==============================================================================
# Crear una nueva publicación (Vender Auto)
# ==============================================================================
@marketplace_bp.route('/', methods=['POST'])
@jwt_required()
def create_listing():
    """
    Crea una nueva publicación de venta de auto.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('title') or not data.get('price'):
        return jsonify({"msg": "Faltan datos obligatorios"}), 400

    new_listing = CarListing(
        user_id=current_user_id,
        title=data['title'],
        brand=data.get('brand', 'Unknown'),
        model=data.get('model', 'Unknown'),
        year=data.get('year', 2000),
        price=data['price'],
        description=data.get('description', ''),
        image_url=data.get('image_url', '')
    )

    try:
        db.session.add(new_listing)
        db.session.commit()
        return jsonify(new_listing.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear la publicación: {str(e)}"}), 500

# ==============================================================================
# Eliminar una publicación (Solo el dueño)
# ==============================================================================
@marketplace_bp.route('/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    current_user_id = get_jwt_identity()
    listing = CarListing.query.get(listing_id)

    if not listing:
        return jsonify({"msg": "Publicación no encontrada"}), 404

    # Verificar que el usuario sea el dueño
    if str(listing.user_id) != str(current_user_id):
        return jsonify({"msg": "No tienes permiso para eliminar esto"}), 403

    try:
        db.session.delete(listing)
        db.session.commit()
        return jsonify({"msg": "Publicación eliminada"}), 200
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500
