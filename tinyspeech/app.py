# TinySpeech Summarizer - Gradio UI Entry Point
# Beautiful web interface for drag-and-drop audio processing

import gradio as gr
import os
import tempfile
import shutil
from pipeline import process_audio
import traceback

def process_audio_file(audio_file):
    """
    Process uploaded audio file and return the generated report
    """
    if audio_file is None:
        return None, "❌ Please upload an audio file first.", ""
    
    try:
        # Create a temporary file with the uploaded audio
        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, "uploaded_audio" + os.path.splitext(audio_file.name)[1])
        
        # Copy uploaded file to temp location
        shutil.copy2(audio_file.name, temp_audio_path)
        
        # Process the audio using our pipeline
        output_path = process_audio(temp_audio_path)
        
        if output_path and os.path.exists(output_path):
            # Read the generated report
            with open(output_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # Clean up temp files
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            success_msg = "✅ Processing complete! Report generated successfully."
            return output_path, success_msg, report_content
        else:
            return None, "❌ Processing failed. Please check your audio file and try again.", ""
            
    except Exception as e:
        error_msg = f"❌ Error processing audio: {str(e)}"
        print(f"Error details: {traceback.format_exc()}")
        return None, error_msg, ""

def create_interface():
    """
    Create and configure the Gradio interface
    """
    
    # Custom CSS for beautiful styling
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    """
    
    with gr.Blocks(css=custom_css, title="TinySpeech Summarizer", theme=gr.themes.Soft()) as interface:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🎵 TinySpeech Summarizer</h1>
            <p>Transform your audio into intelligent summaries, chapters, and transcripts</p>
            <p><em>Fast • Private • Local Processing</em></p>
        </div>
        """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="feature-box">
                    <h3>🚀 How it works:</h3>
                    <ol>
                        <li><strong>Upload</strong> your audio file (MP3, WAV, M4A, etc.)</li>
                        <li><strong>Process</strong> with local Whisper + Gemini AI</li>
                        <li><strong>Download</strong> your beautiful Markdown report</li>
                    </ol>
                </div>
                """)
                
                gr.HTML("""
                <div class="feature-box">
                    <h3>✨ Features:</h3>
                    <ul>
                        <li>🎤 <strong>Accurate Transcription</strong> - Whisper tiny.en</li>
                        <li>📚 <strong>Smart Chapters</strong> - Auto-generated timestamps</li>
                        <li>🤖 <strong>AI Summary</strong> - Key points & topics via Gemini</li>
                        <li>📝 <strong>Markdown Report</strong> - Clean, portable format</li>
                        <li>🔒 <strong>Privacy First</strong> - Local processing</li>
                    </ul>
                </div>
                """)
            
            with gr.Column(scale=2):
                # File upload
                audio_input = gr.File(
                    label="📁 Upload Audio File",
                    file_types=[".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"],
                    type="filepath"
                )
                
                # Process button
                process_btn = gr.Button(
                    "🎵 Process Audio", 
                    variant="primary", 
                    size="lg"
                )
                
                # Status message
                status_msg = gr.Textbox(
                    label="📊 Status",
                    interactive=False,
                    lines=2
                )
                
                # Download section
                with gr.Row():
                    download_file = gr.File(
                        label="📥 Download Report",
                        visible=False
                    )
        
        # Results section
        with gr.Row():
            with gr.Column():
                report_preview = gr.Textbox(
                    label="📄 Report Preview",
                    lines=20,
                    max_lines=30,
                    interactive=False,
                    placeholder="Your generated report will appear here..."
                )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
            <p>🔧 Built with Whisper (OpenAI) + Gemini (Google) + Gradio</p>
            <p><em>Perfect for podcasts, lectures, meetings, and voice memos</em></p>
        </div>
        """)
        
        # Event handlers
        def handle_process(audio_file):
            if audio_file is None:
                return None, "❌ Please upload an audio file first.", "", gr.update(visible=False)
            
            # Show processing message
            yield None, "🔄 Processing your audio... This may take a few minutes.", "", gr.update(visible=False)
            
            # Process the file
            output_path, status, report = process_audio_file(audio_file)
            
            if output_path:
                yield output_path, status, report, gr.update(visible=True, value=output_path)
            else:
                yield None, status, report, gr.update(visible=False)
        
        process_btn.click(
            fn=handle_process,
            inputs=[audio_input],
            outputs=[download_file, status_msg, report_preview, download_file]
        )
        
        # Example files section
        gr.HTML("""
        <div style="margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
            <h4>💡 Tips for best results:</h4>
            <ul>
                <li><strong>Audio Quality:</strong> Clear speech works best (avoid background music)</li>
                <li><strong>Duration:</strong> Works great with 1-60 minute audio files</li>
                <li><strong>Language:</strong> Optimized for English content</li>
                <li><strong>Formats:</strong> Supports MP3, WAV, M4A, FLAC, AAC, OGG</li>
            </ul>
        </div>
        """)
    
    return interface

def main():
    """
    Launch the Gradio web interface
    """
    print("🎵 Starting TinySpeech Summarizer...")
    print("🌐 Web interface will be available at: http://localhost:7860")
    print("📱 Also accessible on your local network for mobile devices")
    print("\n✨ Features ready:")
    print("   🎤 Audio transcription (Whisper tiny.en)")
    print("   📚 Smart chapter generation")
    print("   🤖 AI-powered summaries (Gemini)")
    print("   📝 Beautiful Markdown reports")
    print("\n🚀 Ready to process your audio files!")
    
    interface = create_interface()
    
    # Launch with public sharing disabled by default for privacy
    interface.launch(
        server_name="0.0.0.0",  # Allow access from local network
        server_port=7860,
        share=False,  # Set to True if you want public sharing
        show_error=True
    )

if __name__ == "__main__":
    main()
