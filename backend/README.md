# Backend - Proyecto Programación Web II

Este es el servidor Python (Flask) para el Sistema Full Stack.

## Requisitos
- Python 3.8+

## Instalación

1. Crear entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # Activar:
   # Windows: .\venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configuración:
   Crear un archivo `.env` con:
   ```
   SECRET_KEY=tu_clave
   JWT_SECRET_KEY=tu_jwt_secret
   SQLALCHEMY_DATABASE_URI=sqlite:///local.db
   ```

## Ejecución

```bash
python run.py
```

El servidor iniciará en `http://127.0.0.1:5000`.
