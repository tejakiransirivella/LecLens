# **📹LecLens**
An AI-powered platform that transforms lecture videos into interactive study tools — including auto-generated notes, intelligent Q&amp;A with timestamps, and customizable quizzes. Built with Flask, Flutter, Gemini API, and Whisper.

## **✨Highlights**
- 🎥 **Video Input**: Upload your own video or provide a YouTube link.
- 📄 **Smart Note Generation**: Summarized, structured notes in a PDF-style format.
- 🤖 **AI-Powered Q&A**: Ask questions and get answers with timestamped references.
- 🧩 **Quiz Generator**: Test your knowledge with multiple-choice questions with adjustable difficulty.
- 🔗 **Timestamps**: Jump directly to the moment in the video where the answer was discussed.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Frontend**: Flutter
- **AI & NLP**: Gemini API (for Q&A), Whisper (for transcription)

## **🔧Installation**

### **📋Prerequisites**
Ensure you have the following installed on your system:
- **Python 3**
- **Flutter**
- **Gemini API key**

### **▶️Running the Project**

- **Requirements**:
  This `requirements.txt` file contains all the necessary Python dependencies for the project. Place any additional required dependencies here.

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
    flutter run
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
            llm_wrapper.py
            relevant_time_stamps.py
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
## 🎥 Demo 



