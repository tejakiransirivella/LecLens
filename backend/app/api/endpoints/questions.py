from flask import Blueprint, request, jsonify
from backend.app.services.llm_rag import LLMRAGService
from backend.app.services import relevant_time_stamps
from backend.app.api.cache import Cache

question_bp = Blueprint('question', __name__)

@question_bp.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    session_id = data.get('session_id')
    question = data.get('question')

    if not session_id or not question:
        return jsonify({"error": "Missing session ID or question"}), 400

    # Retrieve transcript
    user = Cache.get_user_cache(session_id)
    transcript_time_stamps = user.get_transcript_timestamps()
    vector_store = user.get_vector_store()

    # Process the question (placeholder for actual logic)
    llm_rag_service = LLMRAGService()
    response = llm_rag_service.answer_user_query(vector_store, question)

    # response = llm_wrapper.answer_user_query(transcript, question)
    sentence_and_time = relevant_time_stamps.find_relevant_sentences(question, transcript_time_stamps)

    conversation = user.get_conversations()
    conversation.append({"USER": question})
    conversation.append({"AI": response})
    user.set_conversations(conversation)

    return jsonify({"session_id": session_id, "relevant_time_stamps": sentence_and_time, "conversation": conversation})
