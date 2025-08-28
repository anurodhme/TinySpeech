# TinySpeech Summarizer - Core Pipeline
# This file contains all functions for transcription, summarization, and file output

import os
import whisper
import google.generativeai as genai
from pydub import AudioSegment
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def load_whisper_model():
    """Load the Whisper tiny.en model for transcription"""
    print("Loading Whisper model...")
    
    # Use local model if available, otherwise download
    local_model_path = os.path.join(os.path.dirname(__file__), 'models', 'tiny.en.pt')
    
    if os.path.exists(local_model_path):
        print(f"Using local model: {local_model_path}")
        model = whisper.load_model(local_model_path)
    else:
        print("Local model not found, downloading...")
        model = whisper.load_model("tiny.en")
    
    print("✓ Whisper model loaded successfully")
    return model

def transcribe_audio(audio_path, model):
    """Transcribe audio file using Whisper"""
    print(f"Transcribing audio: {os.path.basename(audio_path)}")
    
    # Transcribe with timestamps
    result = model.transcribe(audio_path, word_timestamps=True)
    
    # Extract segments with timestamps
    segments = []
    for segment in result['segments']:
        segments.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'].strip()
        })
    
    full_transcript = result['text']
    print(f"✓ Transcription complete ({len(segments)} segments)")
    
    return full_transcript, segments

def generate_chapters(segments, max_chapters=8):
    """Generate timestamped chapters from transcript segments"""
    if not segments:
        return []
    
    # Simple chapter generation: divide transcript into roughly equal time chunks
    total_duration = segments[-1]['end']
    chapter_duration = total_duration / max_chapters
    
    chapters = []
    current_chapter_start = 0
    chapter_text = ""
    
    for i, segment in enumerate(segments):
        chapter_text += segment['text'] + " "
        
        # Check if we should start a new chapter
        if (segment['end'] >= current_chapter_start + chapter_duration and 
            len(chapters) < max_chapters - 1) or i == len(segments) - 1:
            
            # Generate chapter title from first few words
            words = chapter_text.strip().split()[:6]
            title = " ".join(words) + ("..." if len(words) == 6 else "")
            
            chapters.append({
                'start_time': current_chapter_start,
                'end_time': segment['end'],
                'title': title,
                'text': chapter_text.strip()
            })
            
            current_chapter_start = segment['end']
            chapter_text = ""
    
    return chapters

def generate_summary(transcript):
    """Generate summary using Gemini API"""
    print("Generating summary with Gemini...")
    
    prompt = f"""
Please analyze this audio transcript and provide:

1. A concise summary (2-3 paragraphs) of the main content
2. Key points or takeaways (3-5 bullet points)
3. Main topics discussed

Transcript:
{transcript}

Please format your response as:
## Summary
[Your summary here]

## Key Points
- [Point 1]
- [Point 2]
- [Point 3]

## Main Topics
- [Topic 1]
- [Topic 2]
- [Topic 3]
"""
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        print("✓ Summary generated successfully")
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary generation failed. Please check your Gemini API key."

def format_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_markdown_report(transcript, summary, chapters, audio_filename):
    """Create a formatted Markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# TinySpeech Report: {audio_filename}

**Generated:** {timestamp}  
**Source:** {audio_filename}  
**Duration:** {format_timestamp(chapters[-1]['end_time']) if chapters else 'Unknown'}

---

{summary}

---

## 📚 Chapters

"""
    
    # Add chapters
    for i, chapter in enumerate(chapters, 1):
        start_time = format_timestamp(chapter['start_time'])
        end_time = format_timestamp(chapter['end_time'])
        report += f"### {i}. {chapter['title']} ({start_time} - {end_time})\n\n"
    
    report += "\n---\n\n## 📝 Full Transcript\n\n"
    
    # Add full transcript with timestamps
    current_minute = -1
    for segment in chapters:
        # Add minute markers
        segment_minute = int(segment['start_time'] // 60)
        if segment_minute != current_minute:
            current_minute = segment_minute
            report += f"\n**[{format_timestamp(segment['start_time'])}]** "
        
        report += segment['text'] + " "
    
    return report

def process_audio(audio_path):
    """Main pipeline function to process audio file"""
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}")
        return None
    
    print(f"\n🎵 Processing: {os.path.basename(audio_path)}")
    print("=" * 50)
    
    try:
        # Step 1: Load Whisper model
        model = load_whisper_model()
        
        # Step 2: Transcribe audio
        transcript, segments = transcribe_audio(audio_path, model)
        
        # Step 3: Generate chapters
        print("Generating chapters...")
        chapters = generate_chapters(segments)
        print(f"✓ Generated {len(chapters)} chapters")
        
        # Step 4: Generate summary
        summary = generate_summary(transcript)
        
        # Step 5: Create markdown report
        print("Creating markdown report...")
        audio_filename = os.path.basename(audio_path)
        report = create_markdown_report(transcript, summary, chapters, audio_filename)
        
        # Step 6: Save report
        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filename
        base_name = os.path.splitext(audio_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{base_name}_{timestamp}.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Report saved: {output_path}")
        print("\n🎉 Processing complete!")
        
        return output_path
        
    except Exception as e:
        print(f"\n❌ Error processing audio: {e}")
        return None

if __name__ == "__main__":
    # CLI interface for testing
    import sys
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        process_audio(audio_file)
    else:
        print("Usage: python pipeline.py <audio_file_path>")
        print("\nExample: python pipeline.py /path/to/audio.mp3")
