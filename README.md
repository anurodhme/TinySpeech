# TinySpeech Summarizer

A fast, private, local audio processing desktop application that transcribes audio files, generates summaries and chapters, and produces beautifully formatted Markdown reports.

## Features

- **Local Processing**: Uses OpenAI's Whisper tiny.en model for offline transcription
- **AI-Powered Summarization**: Generates concise summaries and key points using Google's Gemini API
- **Chapter Generation**: Automatically creates timestamped chapters for easy navigation
- **Beautiful Reports**: Produces well-formatted Markdown reports with all processed content
- **Web Interface**: User-friendly Gradio UI for drag-and-drop audio processing
- **Fast Performance**: Processes 30-minute audio files in approximately 2 minutes on M-series Macs
- **Privacy Focused**: All processing happens locally, no data leaves your machine

## How It Works

1. **Transcription**: Uses Whisper's tiny.en model to transcribe audio with precise timestamps
2. **Chapter Creation**: Segments the transcript into logical chapters with timestamps
3. **Summarization**: Sends the transcript to Google's Gemini API to generate a comprehensive summary
4. **Report Generation**: Compiles all information into a formatted Markdown report

## Requirements

- Python 3.10 or higher
- M-series Mac (for optimal performance)
- Google Gemini API key
- FFmpeg

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tinyspeech
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg (if not already installed):
   ```bash
   # On macOS with Homebrew
   brew install ffmpeg
   
   # On macOS with Conda
   conda install ffmpeg
   ```

5. Set up your Google Gemini API key:
   - Create a `.env` file in the `tinyspeech/` directory
   - Add your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface (Recommended)

1. Start the Gradio web interface:
   ```bash
   cd tinyspeech
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:7860`

3. Drag and drop an audio file onto the upload area

4. Click "Process Audio" to generate your report

5. Preview the generated report and download it when complete

### Command Line Interface

Process an audio file directly from the command line:

```bash
python pipeline.py /path/to/your/audio/file.mp3
```

The generated report will be saved in the `outputs/` directory.

## Project Structure

```
tinyspeech/
├── app.py              # Gradio web interface
├── pipeline.py         # Core processing pipeline
├── requirements.txt    # Python dependencies
├── .env               # API keys (not included in repo)
├── .gitignore         # Git ignore rules
├── models/            # Local ML models (Whisper tiny.en)
├── outputs/           # Generated reports
└── README.md          # This file
```

## Performance

- The Whisper tiny.en model is optimized for English speech recognition
- Processing time is approximately 1:10 (10 minutes of audio = ~1 minute processing)
- On M-series Macs, processing is accelerated using Metal Performance Shaders

## Privacy & Security

- All audio processing happens locally on your machine
- The Whisper model runs locally and does not send data to external servers
- Only the transcript text is sent to Google's Gemini API for summarization
- API keys are stored locally in the `.env` file and are never shared

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg using Homebrew or Conda
2. **API key errors**: Ensure your `.env` file is correctly configured
3. **Model download failures**: Check your internet connection and try again
4. **Slow processing**: Ensure you're running on an M-series Mac for optimal performance

### Getting Help

If you encounter any issues, please check the existing GitHub issues or create a new one.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the transcription model
- [Google Gemini](https://ai.google.dev/) for the summarization API
- [Gradio](https://gradio.app/) for the web interface framework
