# **📹LecLens**
An AI-powered platform that transforms lecture videos into interactive study tools — including auto-generated notes, intelligent Q&amp;A with timestamps, and customizable quizzes. It internally uses RAG(Retrieval-Augmented Generation) with a FAISS vector database for fast, accurate responses. Built with Flask, Flutter, langChain, Gemini API, and Whisper and deployed on AWS with a live demo.

## **✨Highlights**
- 🎥 **Video Input**: Upload your own video or provide a YouTube link.
- 📄 **Smart Note Generation**: Summarized, structured notes in a PDF-style format using advanced LLM summarization.
- 🤖 **AI-Powered Q&A with RAG**: Ask questions and get accurate answers based on FAISS vector similarity search and Gemini 2.0 LLM with timestamped references.
- 🧩 **Quiz Generator**: Test your knowledge with multiple-choice questions with adjustable difficulty.
- 🔗 **Timestamps**: Jump directly to the moment in the video where the answer was discussed.
- ☁️ **Deployed on AWS**: Live site running on EC2 with Docker.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Frontend**: Flutter
- **AI & NLP**: Gemini API (for Q&A), Whisper (for transcription), LangChain (for RAG), FAISS (vector store)
- **Deployment**: AWS EC2, Docker, S3 (for config)

## **🔧Installation**

### **⚙️Configuration**
This project loads environment variables from a `.env` file stored in AWS S3.
For local development, you have two options:
- **Manual**: Place your .env file in the backend root folder (same level as run.py).
- **Automatic (if using AWS credentials)**:The backend will attempt to download `.env` from S3 — for this, you must:
    - Set up AWS CLI credentials (`~/.aws/credentials`)
    - Ensure your IAM user has `s3:GetObject` permission for the S3 bucket used in the project.

### **📋Prerequisites**
Ensure you have the following installed on your system:
- **Docker**
- **Python 3**
- **Flutter**
- **Gemini API key in .env file**
- **VIDCAP_API_KEY in .env file**

### **▶️Run with Docker Compose**
```bash
docker-compose up --build
```
That’s it — the backend and frontend will start up, and you can access the app at:
http://localhost:8080/


### **▶️Run Manually (For Development)**

- **Requirements**:
  The backend/requirements.txt file contains all necessary Python dependencies.

- **Set up backend**:
    ```bash 
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py
    ```
- **Set up frontend**:
    ```bash 
    cd frontend/flutter_app
    flutter pub get
    flutter run -d <browser>
    ```

## **🗂️Project Structure**

- **backend**
    ```bash
    app
    │   app.py
    │   
    ├───api
    │   │   cache.py
    │   │   user.py
    │   │   
    │   └───endpoints
    │           notes.py
    │           questions.py
    │           quiz.py
    │           upload.py
    │
    └───services
            llm_rag.py
            relevant_time_stamps.py
            s3_service.py
            transcript_extraction.py
            youtube_transcript.py
    ```
- **frontend**
    ```bash
    │   main.dart
    │   
    ├───components
    │       button.dart
    │       common_background.dart
    │       square_tile.dart
    │       
    ├───pages
    │       chat_page.dart
    │       
    └───transcripts
            transcript_item.dart
    ```
## **🚀Live Demo**
Check out the live demo of LecLens at [Live LecLens Demo](http://ec2-3-19-76-44.us-east-2.compute.amazonaws.com:8080/).


