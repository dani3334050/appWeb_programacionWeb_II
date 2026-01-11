from app import db
from datetime import datetime

# ==============================================================================
# Modelo User (Usuario)
# ==============================================================================
class User(db.Model):
    """
    Representa a los usuarios del sistema (administradores, mecánicos, recepción).
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False)    # Correo electrónico único
    password_hash = db.Column(db.String(255), nullable=False)         # Contraseña hasheada
    role = db.Column(db.String(20), nullable=False, default='recepcion')  # Roles: admin, mecanico, recepcion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # Fecha de creación

    # Relación inversa: Un usuario puede crear muchas órdenes de trabajo
    work_orders = db.relationship('WorkOrder', backref='creator', lazy=True)

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ==============================================================================
# Modelo Client (Cliente)
# ==============================================================================
class Client(db.Model):
    """
    Representa a los clientes del taller.
    """
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)  # Nombre
    last_name = db.Column(db.String(50), nullable=False)   # Apellido
    email = db.Column(db.String(120), unique=True, nullable=True) # Email opcional pero único si existe
    phone = db.Column(db.String(20), nullable=True)        # Teléfono de contacto
    address = db.Column(db.String(200), nullable=True)     # Dirección física
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación: Un cliente tiene varios vehículos
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ==============================================================================
# Modelo Vehicle (Vehículo)
# ==============================================================================
class Vehicle(db.Model):
    """
    Representa los vehículos que ingresan al taller.
    """
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False) # Relación con Cliente
    plate = db.Column(db.String(20), unique=True, nullable=False) # Placa única
    brand = db.Column(db.String(50), nullable=False)              # Marca
    model = db.Column(db.String(50), nullable=False)              # Modelo
    year = db.Column(db.Integer, nullable=False)                  # Año
    vin = db.Column(db.String(50), unique=True, nullable=True)    # Número de chasis (VIN)

    # Relación: Un vehículo puede tener muchas órdenes de trabajo
    work_orders = db.relationship('WorkOrder', backref='vehicle', lazy=True)

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'plate': self.plate,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'vin': self.vin
        }

# ==============================================================================
# Modelo Service (Servicio)
# ==============================================================================
class Service(db.Model):
    """
    Catálogo de servicios disponibles (ej: Cambio de aceite, Afinación).
    """
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)           # Nombre del servicio
    description = db.Column(db.Text, nullable=True)            # Descripción detallada
    base_price = db.Column(db.Float, nullable=False, default=0.0) # Precio base sugerido

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price
        }

# ==============================================================================
# Modelo WorkOrder (Orden de Trabajo)
# ==============================================================================
class WorkOrder(db.Model):
    """
    Cabecera de la orden de trabajo.
    """
    __tablename__ = 'work_orders'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False) # Vehículo a reparar
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)       # Usuario que creó la orden
    status = db.Column(db.String(20), default='pendiente') # Estados: pendiente, en_progreso, finalizado
    total = db.Column(db.Float, default=0.0)               # Total monetario de la orden
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Fecha de creación

    # Relación: Una orden tiene muchos items (servicios)
    items = db.relationship('OrderItem', backref='work_order', lazy=True)

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'user_id': self.user_id,
            'status': self.status,
            'total': self.total,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items] # Incluir items anidados
        }

# ==============================================================================
# Modelo OrderItem (Item de Orden)
# ==============================================================================
class OrderItem(db.Model):
    """
    Detalle de la orden de trabajo (relación muchos a muchos entre Orden y Servicio con precio histórico).
    """
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False) # Orden padre
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)       # Servicio realizado
    price_at_moment = db.Column(db.Float, nullable=False) # Precio congelado al momento de la orden

    # Relación para acceder a info del servicio desde el item
    service = db.relationship('Service')

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'work_order_id': self.work_order_id,
            'service_id': self.service_id,
            'service_name': self.service.name if self.service else None, # Helper para frontend
            'price_at_moment': self.price_at_moment
        }
