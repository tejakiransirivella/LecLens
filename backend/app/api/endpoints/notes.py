from flask import Blueprint, request, jsonify
from backend.app.services.llm_rag import LLMRAGService
from backend.app.api.cache import Cache
from backend.app.api.user import User

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['POST'])
def get_notes():
    data = request.json
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({"error": "Missing session ID"}), 400

    # Retrieve transcript from cache
    user: User = Cache.get_user_cache(session_id)

    if user.get_notes() is not None:
        return jsonify({"session_id": session_id, "notes": user.get_notes()})
    
    vector_store = user.get_vector_store()

    llm_rag_service = LLMRAGService()
    notes = llm_rag_service.generate_notes(vector_store)
    user.set_notes(notes)

    return jsonify({"session_id": session_id, "notes": notes})
