from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# Creamos el Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ==============================================================================
# Endpoint: Registro de Usuario
# ==============================================================================
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo usuario en el sistema.
    Espera un JSON con: username, email, password, role (opcional).
    """
    data = request.get_json()

    # Validaciones básicas de entrada
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Faltan datos obligatorios"}), 400

    # Verificar si el usuario o email ya existen
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "El nombre de usuario ya existe"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "El correo electrónico ya está registrado"}), 400

    # Crear el nuevo usuario
    # Hasheamos la contraseña por seguridad antes de guardarla
    hashed_password = generate_password_hash(data['password'])
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=data.get('role', 'recepcion') # Rol por defecto: recepcion
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Usuario registrado exitosamente", "user": new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al registrar usuario: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Login (Inicio de Sesión)
# ==============================================================================
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica un usuario y devuelve un token JWT.
    Espera un JSON con: email, password.
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Faltan credenciales"}), 400

    # Buscar usuario por email
    user = User.query.filter_by(email=data['email']).first()

    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    # Crear el token de acceso
    # Usamos el ID del usuario como identidad en el token
    # Identity puede ser cualquier dato serializable, el ID es lo más común
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    return jsonify({
        "msg": "Inicio de sesión exitoso",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

# ==============================================================================
# Endpoint: Obtener Usuario Actual (Protected)
# ==============================================================================
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Devuelve la información del usuario actualmente autenticado.
    Requiere un token JWT válido en el header Authorization.
    """
    # Obtener la identidad del token (el ID del usuario que guardamos en login)
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200
