from flask import Blueprint, request, jsonify
import uuid  # For generating session IDs
from backend.app.services import youtube_transcript
from backend.app.services import transcript_extraction
from backend.app.api.cache import Cache
from backend.app.services.llm_rag import LLMRAGService
from backend.app.api.user import User

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    data = request.json
    youtube_url = data.get('youtube_url')
    video_file = data.get('video_file')

    if not youtube_url and not video_file:
        return jsonify({"error": "Provide either a YouTube URL or a video file"}), 400

    # Generate session ID
    user:User = Cache.get_user_cache()
    session_id = user.get_sessionId()


    if youtube_url:
        transcript_time_stamps, transcript_str = youtube_transcript.get_transcript(youtube_url)
    else:
        transcript_time_stamps, transcript_str = transcript_extraction.get_transcript_from_file(video_file)

    if not transcript_time_stamps or not transcript_str:
        return jsonify({"error": "Failed to extract transcript, Try again later."}), 500
    
    user.set_transcript(transcript_str)
    user.set_transcript_timestamps(transcript_time_stamps)

    llm_rag_service = LLMRAGService()
    vector_store = llm_rag_service.create_vector_store(transcript_str)
    user.set_vector_store(vector_store)

    return jsonify({"session_id": session_id, "message": "Video processed and transcript stored."})
