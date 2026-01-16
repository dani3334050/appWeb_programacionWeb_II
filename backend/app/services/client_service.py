from app import db
from app.models import Client, Vehicle
from sqlalchemy.exc import IntegrityError

class ClientService:
    """
    Servicio para la gestión de Clientes y sus Vehículos.
    """

    @staticmethod
    def create_client(first_name, last_name, email=None, phone=None, address=None):
        """
        Crea un nuevo cliente.

        Args:
            first_name (str): Nombre.
            last_name (str): Apellido.
            email (str, optional): Email.
            phone (str, optional): Teléfono.
            address (str, optional): Dirección.

        Returns:
            Client: Cliente creado.

        Raises:
            ValueError: Si el email ya existe (IntegrityError).
        """
        new_client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )
        try:
            db.session.add(new_client)
            db.session.commit()
            return new_client
        except IntegrityError:
            db.session.rollback()
            raise ValueError("El email ya está registrado para otro cliente")

    @staticmethod
    def get_all_clients():
        """Retorna todos los clientes registrados."""
        return Client.query.all()
        
    @staticmethod
    def get_client_by_id(client_id):
        """Retorna un cliente por ID."""
        return Client.query.get(client_id)

    @staticmethod
    def update_client(client_id, data):
        """
        Actualiza los datos de un cliente.

        Args:
            client_id (int): ID del cliente.
            data (dict): Campos a actualizar (first_name, last_name, email, phone, address).

        Returns:
            Client: Cliente actualizado.

        Raises:
            ValueError: Si el cliente no existe o email duplicado.
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Cliente no encontrado")

        if 'first_name' in data:
            client.first_name = data['first_name']
        if 'last_name' in data:
            client.last_name = data['last_name']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']
        if 'address' in data:
            client.address = data['address']

        try:
            db.session.commit()
            return client
        except IntegrityError:
            db.session.rollback()
            raise ValueError("El email ya está registrado para otro cliente")

    @staticmethod
    def delete_client(client_id):
        """
        Elimina un cliente y, por cascada, sus vehículos si la relación lo permite.

        Raises:
            ValueError: Si el cliente no existe.
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Cliente no encontrado")
        db.session.delete(client)
        db.session.commit()

    @staticmethod
    def add_vehicle(client_id, plate, brand, model, year, vin=None):
        """
        Asocia un vehículo a un cliente.

        Args:
            client_id (int): ID del cliente dueño.
            plate (str): Placa.
            brand (str): Marca.
            model (str): Modelo.
            year (int): Año.
            vin (str, optional): VIN.

        Returns:
            Vehicle: Vehículo creado.

        Raises:
            ValueError: Si cliente no existe o placa/VIN duplicados.
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Cliente no encontrado")

        new_vehicle = Vehicle(
            client_id=client_id,
            plate=plate,
            brand=brand,
            model=model,
            year=year,
            vin=vin
        )

        try:
            db.session.add(new_vehicle)
            db.session.commit()
            return new_vehicle
        except IntegrityError:
            db.session.rollback()
            raise ValueError("La placa o el VIN ya existen")

    @staticmethod
    def get_client_vehicles(client_id):
        """
        Obtiene los vehículos de un cliente específico.
        
        Raises:
            ValueError: Si el cliente no existe.
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Cliente no encontrado")
        return client.vehicles
    
    @staticmethod
    def get_all_vehicles():
        """
        Retorna todos los vehículos registrados en el sistema,
        incluyendo la información de su dueño.
        """
        return Vehicle.query.all()

    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        """Retorna un vehículo por ID."""
        return Vehicle.query.get(vehicle_id)

    @staticmethod
    def update_vehicle(vehicle_id, data):
        """
        Actualiza los datos de un vehículo existente.

        Args:
            vehicle_id (int): ID del vehículo.
            data (dict): Diccionario con los campos a actualizar.

        Returns:
            Vehicle: Vehículo actualizado.

        Raises:
            ValueError: Si el vehículo no existe o hay conflictos de unicidad.
        """
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            raise ValueError("Vehículo no encontrado")

        # Actualizar campos permitidos
        if 'plate' in data:
            vehicle.plate = data['plate']
        if 'brand' in data:
            vehicle.brand = data['brand']
        if 'model' in data:
            vehicle.model = data['model']
        if 'year' in data:
            vehicle.year = data['year']
        if 'vin' in data:
            vehicle.vin = data['vin']
        # Nota: Permitir cambiar el cliente (client_id) podría ser útil, 
        # pero requiere validación extra. Lo incluiremos si se solicita.
        if 'client_id' in data:
            # Validar que el cliente exista
            client = Client.query.get(data['client_id'])
            if not client:
                raise ValueError("El cliente asignado no existe")
            vehicle.client_id = data['client_id']

        try:
            db.session.commit()
            return vehicle
        except IntegrityError:
            db.session.rollback()
            raise ValueError("La placa o el VIN ya existen en otro vehículo")

    @staticmethod
    def delete_vehicle(vehicle_id):
        """
        Elimina un vehículo del sistema.

        Args:
            vehicle_id (int): ID del vehículo.

        Raises:
            ValueError: Si el vehículo no existe.
        """
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            raise ValueError("Vehículo no encontrado")

        db.session.delete(vehicle)
        db.session.commit()
