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
    /* Header styling */
    .header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Feature box styling */
    .feature-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid #d0d7de;
        color: #24292f;
    }
    
    /* Feature box headings */
    .feature-box h3 {
        color: #0969da;
        margin-top: 0;
        font-weight: 600;
    }
    
    /* Feature box lists */
    .feature-box ol, .feature-box ul {
        color: #24292f;
        padding-left: 1.5rem;
    }
    
    .feature-box li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
        color: #24292f;
    }
    
    .feature-box ol li {
        color: #24292f;
        font-weight: 500;
    }
    
    .feature-box ol li strong {
        color: #0969da;
    }
    
    /* Status messages */
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #4e54c8;
        margin: 1rem 0;
        background: #f5f7ff;
        color: #24292f;
    }
    .status-success {
        color: #155724;
        background-color: #d4edda;
        font-weight: bold;
    }
    .status-error {
        color: #721c24;
        background-color: #f8d7da;
        font-weight: bold;
    }
    
    /* Body background */
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
        color: #24292f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Button styling */
    button {
        background: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
    }
    
    /* Input styling */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #24292f !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
    }
    
    /* Gradio container */
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Strong text */
    strong {
        color: #24292f;
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
                        <li><strong style="color: #0969da;">Upload</strong> your audio file (MP3, WAV, M4A, etc.)</li>
                        <li><strong style="color: #0969da;">Process</strong> with local Whisper + Gemini AI</li>
                        <li><strong style="color: #0969da;">Download</strong> your beautiful Markdown report</li>
                    </ol>
                </div>
                """)
                
                gr.HTML("""
                <div class="feature-box">
                    <h3>✨ Features:</h3>
                    <ul>
                        <li>🎤 <strong style="color: #0969da;">Accurate Transcription</strong> - Whisper tiny.en</li>
                        <li>📚 <strong style="color: #0969da;">Smart Chapters</strong> - Auto-generated timestamps</li>
                        <li>🤖 <strong style="color: #0969da;">AI Summary</strong> - Key points & topics via Gemini</li>
                        <li>📝 <strong style="color: #0969da;">Markdown Report</strong> - Clean, portable format</li>
                        <li>🔒 <strong style="color: #0969da;">Privacy First</strong> - Local processing</li>
                    </ul>
                </div>
                """),
            
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
        <div style="margin-top: 2rem; padding: 1rem; background: #8c2222; border-radius: 8px; border: 1px solid #d0d7de; box-shadow: 0 2px 8px rgba(0,0,0,0.1); color: #ffffff;">
            <h4 style="color: #0969da; margin-top: 0; font-weight: bold;">💡 Tips for best results:</h4>
            <ul style="color: #0969da; padding-left: 1.5rem; font-weight: bold;">
                <li style="margin-bottom: 0.5rem;"><strong style="color: #0969da; font-weight: bold;">Audio Quality:</strong> Clear speech works best (avoid background music)</li>
                <li style="margin-bottom: 0.5rem;"><strong style="color: #0969da; font-weight: bold;">Duration:</strong> Works great with 1-60 minute audio files</li>
                <li style="margin-bottom: 0.5rem;"><strong style="color: #0969da; font-weight: bold;">Language:</strong> Optimized for English content</li>
                <li><strong style="color: #0969da; font-weight: bold;">Formats:</strong> Supports MP3, WAV, M4A, FLAC, AAC, OGG</li>
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
        server_port=7861,
        share=False,  # Set to True if you want public sharing
        quiet=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
