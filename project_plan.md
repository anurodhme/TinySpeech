Project Plan: TinySpeech Summarizer
Version: 1.2

Date: August 28, 2025

Status: Planning

1. Overview
TinySpeech is a desktop application designed for fast, private, and local audio processing. It takes any audio file—such as a podcast, lecture, or meeting—and produces a concise summary, timestamped chapters, and a full verbatim transcript.

The pipeline prioritizes privacy and performance by using an on-device Whisper model for transcription and the efficient Gemini API for high-quality summarization. The final output is a clean, portable Markdown report, perfect for notes, documentation, or sharing.

Target Platform: M-series Macs (8 GB RAM minimum)

Key Performance Goal: Process a 30-minute audio file in approximately 2 minutes.

Primary Interface: A simple, intuitive drag-and-drop web UI.

2. Technical Specifications
2.1. Technology Stack
Language: Python 3.10+

Transcription: openai-whisper (tiny.en model)

Summarization: google-genai (Gemini 2.5 Flash)

Audio Handling: pydub, ffmpeg

Core Libraries: torch (CPU), numpy

UI & Configuration: gradio, python-dotenv

2.2. Project Structure
The project is organized into functional modules to separate the core logic from the user interface, ensuring maintainability.

tinyspeech/
├── app.py              # Gradio UI entry point
├── pipeline.py         # Core transcription & summarization logic
├── models/             # Directory for cached ML models
├── outputs/            # Directory for generated .md reports
├── requirements.txt    # List of all Python dependencies
└── .env                # For storing the GEMINI_API_KEY

3. Development Roadmap (MVP)
Milestone 1: Core Pipeline Implementation
Task: Implement the pipeline.py module, containing all functions for transcription, summarization, and file output.

Goal: Create a functional command-line interface (CLI) that can process an audio file and generate a complete Markdown report.

Milestone 2: Gradio UI Development
Task: Build the app.py file to create a user-friendly web interface.

Goal: Allow users to drag and drop an audio file, see the results displayed in the UI, and download the generated report.

Milestone 3: Documentation & Refinement
Task: Create a comprehensive README.md with clear setup and usage instructions.

Goal: Ensure a new user can clone the repository and have the application running within five minutes.

4. Future Enhancements (Post-MVP)
The following features are planned for future releases to extend the application's capabilities:

Speaker Diarization: Integrate a library to identify and label different speakers.

Cloud Export: Add functionality to push reports directly to services like Notion.

System Integration: Develop a macOS Shortcut to share Voice Memos directly to the app.

Batch Processing: Create a script to automatically process all new files in a designated folder.

Standalone Application: Package the project into a distributable .dmg file so it can be run without installing Python.

5. Setup & Execution
5.1. Initial Setup
Clone Repository: git clone https://github.com/<your-repo>/tinyspeech.git

Install Dependencies: pip install -r requirements.txt

Install Audio Codecs: brew install ffmpeg

Configure API Key: Create a .env file and add your GEMINI_API_KEY.

5.2. Running the Application
GUI Mode: python app.py

CLI Mode: python -c "import pipeline; pipeline.process('path/to/audio.mp3')"