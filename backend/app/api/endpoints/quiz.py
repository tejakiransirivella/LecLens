from flask import Blueprint, request, jsonify
from backend.app.services import llm_wrapper
from backend.app.api.cache import Cache
from backend.app.api.user import User

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz', methods=['POST'])
def get_quiz():
    data = request.json
    session_id = data.get('session_id')
    difficulty_level = data.get('difficulty_level')

    if not session_id:
        return jsonify({"error": "Missing session ID"}), 400

    # Retrieve transcript from cache
    user:User = Cache.get_user_cache(session_id)
    transcript = user.get_transcript()

    quiz = llm_wrapper.generate_quiz(transcript,difficulty_level)

    return jsonify({"session_id": session_id, "quiz": quiz})