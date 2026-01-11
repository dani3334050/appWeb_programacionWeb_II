from flask import Blueprint, request, jsonify

# Creamos el Blueprint para las rutas de IA
ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

# ==============================================================================
# Endpoint: Preguntar a la IA (Mock)
# ==============================================================================
@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    """
    Recibe una pregunta y devuelve una respuesta simulada.
    Preparado para integrar modelos LLM (LangChain, OpenAI, etc.).
    """
    data = request.get_json()
    
    # Validar entrada
    if not data or not data.get('question'):
        return jsonify({"msg": "Se requiere una pregunta (field: question)"}), 400

    question = data['question']
    context = data.get('context', '') # Contexto opcional (ej: historial de chat)

    # TODO: Implementar LangChain aquí
    # Aquí es donde conectaríamos con OpenAI/Anthropic/Gemini usando LangChain.
    # Podríamos usar el 'context' para RAG (Retrieval Augmented Generation).

    # Respuesta simulada por ahora
    mock_response = f"El backend recibió tu pregunta sobre: {question}"

    return jsonify({
        "response": mock_response,
        "question_received": question
    }), 200
