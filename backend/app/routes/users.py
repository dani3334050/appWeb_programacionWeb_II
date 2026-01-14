from flask import Blueprint, jsonify
from app.models import User
from app import db

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/technicians', methods=['GET'])
def get_technicians():
    try:
        # Fetch users with role 'mecanico'
        technicians = User.query.filter_by(role='mecanico').all()
        
        # Transform to list of dicts with MOCK data for UI visualization (as requested by design)
        # In a real app, these fields would be in a separate Profile model
        tech_list = []
        import random
        
        specialties = ["Mecánica General", "Transmisión", "Electricidad", "Diagnóstico", "Chapistería", "Pintura", "Frenos", "Suspensión"]
        certifications = ["ASE, Toyota Certified", "ASE, Bosch Certified", "I-CAR", "ASE"]
        statuses = ["Disponible", "Ocupado", "Ausente"]
        
        for tech in technicians:
            # Deterministic mock data based on ID for consistency
            random.seed(tech.id) 
            
            tech_data = {
                "id": tech.id,
                "first_name": tech.username.split(' ')[0] if ' ' in tech.username else tech.username,
                "last_name": tech.username.split(' ')[1] if ' ' in tech.username else "",
                "email": tech.email,
                "role": tech.role,
                # Mock fields for UI design matching
                "specialties": random.sample(specialties, k=random.randint(1, 2)),
                "status": random.choice(statuses),
                "certification": random.choice(certifications),
                "jobs_month": random.randint(20, 60),
                "rating": round(random.uniform(4.0, 5.0), 1)
            }
            tech_list.append(tech_data)
            
        return jsonify(tech_list), 200
    except Exception as e:
        return jsonify({"msg": f"Error al obtener técnicos: {str(e)}"}), 500
