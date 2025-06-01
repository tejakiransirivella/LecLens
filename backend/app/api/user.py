class User:

    def __init__(self, sessionId):
        self.sessionId = sessionId
        self.transcript_timestamps = None
        self.transcript = None
        self.conversations = []
        self.vector_store = None
        self.notes = None

    def get_sessionId(self):
        return self.sessionId

    def set_transcript(self, transcript):
        self.transcript = transcript
    
    def set_transcript_timestamps(self, transcript_timestamps):
        self.transcript_timestamps = transcript_timestamps
    
    def set_conversations(self, conversations):
        self.conversations = conversations
    
    def get_transcript(self):
        return self.transcript

    def get_transcript_timestamps(self):
        return self.transcript_timestamps
    
    def get_conversations(self):
        return self.conversations
    
    def get_vector_store(self):
        return self.vector_store
    
    def set_vector_store(self, vector_store):
        self.vector_store = vector_store

    def set_notes(self, notes):
        self.notes = notes

    def get_notes(self):
        return self.notes