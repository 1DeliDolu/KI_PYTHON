#!/usr/bin/env python3
"""
Multi-Task AI Assistant - Modern Gradio Web Interface
A comprehensive AI assistant with modern web interface for multiple tasks including
Wikipedia queries, document processing, image analysis, video analysis, and translation.
"""

import gradio as gr
import os
import sys
import logging
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from config import Config
from scripts.wikipedia_query import WikipediaQuery
from scripts.translator import Translator
from scripts.document_reader import DocumentReader
from scripts.image_analysis import ImageAnalysis
from scripts.video_analysis import VideoAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GradioAIAssistant:
    def __init__(self):
        """Initialize the Gradio AI Assistant"""
        self.config = Config()
        
        # Initialize modules
        try:
            self.wikipedia = WikipediaQuery()
            self.translator = Translator()
            self.doc_reader = DocumentReader()
            self.image_analyzer = ImageAnalysis()
            self.video_analyzer = VideoAnalysis()
            logger.info("All modules initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing modules: {e}")
    
    def search_wikipedia(self, query: str, max_results: int = 3) -> Tuple[str, str]:
        """Search Wikipedia and return formatted results with status"""
        if not query.strip():
            return "❌ Error", "Please enter a search query."
        
        try:
            result = self.wikipedia.search(query, max_results=max_results)
            
            if not result["success"]:
                return "❌ Error", f"Error: {result['message']}"
            
            if not result["results"]:
                return "⚠️ Warning", f"No results found for '{query}'"
            
            # Format results with modern styling
            output = f"""
# 🔍 Wikipedia Search Results
**Query:** `{query}`  
**Found:** {len(result["results"])} article(s)

---
"""
            
            for i, article in enumerate(result["results"], 1):
                output += f"""
## {i}. {article['title']}

📖 **Summary:**  
{article['summary'][:400]}...

🔗 **[Read Full Article]({article['url']})**

---
"""
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return "❌ Error", f"Error searching Wikipedia: {str(e)}"
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = "auto") -> Tuple[str, str]:
        """Translate text between languages with modern output"""
        if not text.strip():
            return "❌ Error", "Please enter text to translate."
        
        if not target_lang:
            return "❌ Error", "Please select a target language."
        
        try:
            result = self.translator.translate(text, target_lang, source_lang)
            
            if not result["success"]:
                return "❌ Error", f"Translation Error: {result['message']}"
            
            # Modern translation output with cards
            output = f"""
# 🌐 Translation Complete

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px;">
<h3>🔤 Original</h3>
<p><strong>Language:</strong> {result.get('source_language', 'auto').upper()}</p>
<p><em>"{result['original_text']}"</em></p>
</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 15px;">
<h3>✨ Translated</h3>
<p><strong>Language:</strong> {result['target_language'].upper()}</p>
<p><em>"{result['translated_text']}"</em></p>
</div>

</div>

**Service:** {result.get('service', 'Unknown')} | **Time:** {time.strftime('%H:%M:%S')}
"""
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return "❌ Error", f"Error translating text: {str(e)}"
    
    def detect_language(self, text: str) -> Tuple[str, str]:
        """Detect the language of given text with modern output"""
        if not text.strip():
            return "❌ Error", "Please enter text for language detection."
        
        try:
            result = self.translator.detect_language(text)
            
            if not result["success"]:
                return "❌ Error", f"Detection Error: {result['message']}"
            
            # Modern detection output
            output = f"""
# 🔍 Language Detection Complete

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
    <h3>🎯 Detection Results</h3>
    <p><strong>Text Sample:</strong> <em>"{text[:150]}{'...' if len(text) > 150 else ''}"</em></p>
    <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h4>🌍 Detected Language</h4>
            <p style="font-size: 1.3em; margin: 5px 0;">{result.get('language_name', 'Unknown')} ({result.get('detected_language', 'unknown')})</p>
        </div>
        <div style="text-align: right;">
            <h4>📊 Confidence</h4>
            <p style="font-size: 1.3em; margin: 5px 0;">{result.get('confidence', 0):.1%}</p>
        </div>
    </div>
</div>

**Analysis Time:** {time.strftime('%H:%M:%S')}
"""
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return "❌ Error", f"Error detecting language: {str(e)}"
    
    def process_document(self, file) -> Tuple[str, str]:
        """Process uploaded document and extract content with modern output"""
        if file is None:
            return "❌ Error", "Please upload a document file."
        
        try:
            # Get file path
            file_path = file.name if hasattr(file, 'name') else str(file)
            
            result = self.doc_reader.read_document(file_path)
            
            if not result["success"]:
                return "❌ Error", f"Document Processing Error: {result['message']}"
            
            content = result["content"]
            metadata = result.get("metadata", {})
            
            # Modern document analysis output
            output = f"""
# 📄 Document Analysis Complete

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
    <h3>📊 Document Overview</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
        <div style="text-align: center;">
            <h4>📁 File</h4>
            <p>{Path(file_path).name}</p>
        </div>
        <div style="text-align: center;">
            <h4>📋 Type</h4>
            <p>{metadata.get('file_type', 'Unknown')}</p>
        </div>
        <div style="text-align: center;">
            <h4>💾 Size</h4>
            <p>{metadata.get('file_size_mb', 0):.2f} MB</p>
        </div>
        <div style="text-align: center;">
            <h4>📄 Pages</h4>
            <p>{metadata.get('page_count', 'N/A')}</p>
        </div>
    </div>
</div>

## 📖 Content Preview
```
{content[:1500]}{'...' if len(content) > 1500 else ''}
```

**Extraction Time:** {time.strftime('%H:%M:%S')} | **Characters:** {len(content):,}
"""
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Document processing error: {e}")
            return "❌ Error", f"Error processing document: {str(e)}"
    
    def analyze_image(self, image) -> Tuple[str, str]:
        """Analyze uploaded image with modern output"""
        if image is None:
            return "❌ Error", "Please upload an image file."
        
        try:
            # Save temporary file if needed
            if hasattr(image, 'name'):
                image_path = image.name
            else:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    if hasattr(image, 'save'):
                        image.save(tmp.name)
                    image_path = tmp.name
            
            result = self.image_analyzer.analyze_image(image_path)
            
            if not result["success"]:
                return "❌ Error", f"Image Analysis Error: {result['message']}"
            
            analysis = result["analysis"]
            basic_info = analysis.get("basic_info", {})
            color_analysis = analysis.get("color_analysis", {})
            
            # Modern image analysis output
            output = f"""
# 🖼️ Image Analysis Complete

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
    <h3>🎨 Image Properties</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 15px 0;">
        <div style="text-align: center;">
            <h4>📐 Dimensions</h4>
            <p>{basic_info.get('width', 'N/A')} × {basic_info.get('height', 'N/A')}</p>
        </div>
        <div style="text-align: center;">
            <h4>🎭 Format</h4>
            <p>{basic_info.get('format', 'Unknown')}</p>
        </div>
        <div style="text-align: center;">
            <h4>🌈 Mode</h4>
            <p>{basic_info.get('mode', 'Unknown')}</p>
        </div>
        <div style="text-align: center;">
            <h4>💾 Size</h4>
            <p>{basic_info.get('file_size_mb', 0):.2f} MB</p>
        </div>
    </div>
</div>

## 🎨 Color Analysis
"""
            
            if color_analysis:
                output += f"""
- **✨ Average Brightness:** {color_analysis.get('average_brightness', 'N/A')}
- **🌈 Dominant Colors:** {len(color_analysis.get('dominant_colors', []))} detected
- **📊 Color Diversity:** {color_analysis.get('color_diversity', 'N/A')}
"""
            else:
                output += "Color analysis not available"
            
            output += f"\n\n**Analysis Time:** {time.strftime('%H:%M:%S')}"
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return "❌ Error", f"Error analyzing image: {str(e)}"
    
    def analyze_video(self, video) -> Tuple[str, str]:
        """Analyze uploaded video with modern output"""
        if video is None:
            return "❌ Error", "Please upload a video file."
        
        try:
            # Get video path
            video_path = video.name if hasattr(video, 'name') else str(video)
            
            result = self.video_analyzer.analyze_video(video_path)
            
            if not result["success"]:
                return "❌ Error", f"Video Analysis Error: {result['message']}"
            
            analysis = result["analysis"]
            basic_info = analysis.get("basic_info", {})
            audio_info = analysis.get("audio_analysis", {})
            
            # Modern video analysis output
            output = f"""
# 🎥 Video Analysis Complete

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
    <h3>🎬 Video Properties</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 15px 0;">
        <div style="text-align: center;">
            <h4>⏱️ Duration</h4>
            <p>{basic_info.get('duration_formatted', 'N/A')}</p>
        </div>
        <div style="text-align: center;">
            <h4>📺 Resolution</h4>
            <p>{basic_info.get('resolution', 'N/A')}</p>
        </div>
        <div style="text-align: center;">
            <h4>🎞️ FPS</h4>
            <p>{basic_info.get('fps', 'N/A')}</p>
        </div>
        <div style="text-align: center;">
            <h4>💾 Size</h4>
            <p>{basic_info.get('file_size_mb', 0):.2f} MB</p>
        </div>
        <div style="text-align: center;">
            <h4>🖼️ Frames</h4>
            <p>{basic_info.get('frame_count', 'N/A'):,}</p>
        </div>
    </div>
</div>

## 🎵 Audio Analysis
"""
            
            if audio_info.get('has_audio'):
                output += f"""
✅ **Audio Track Found**
- **Sample Rate:** {audio_info.get('sample_rate', 'N/A')} Hz
- **Channels:** {audio_info.get('channels', 'N/A')}
- **Duration:** {audio_info.get('duration', 'N/A')} seconds
"""
            else:
                output += "❌ **No Audio Track**"
            
            output += f"\n\n**Analysis Time:** {time.strftime('%H:%M:%S')}"
            
            return "✅ Success", output
            
        except Exception as e:
            logger.error(f"Video analysis error: {e}")
            return "❌ Error", f"Error analyzing video: {str(e)}"

def create_gradio_interface():
    """Create and configure the modern Gradio interface"""
    
    # Initialize the assistant
    assistant = GradioAIAssistant()
    
    # Language options for translation
    languages = {
        "🇹🇷 Turkish": "tr", "🇺🇸 English": "en", "🇩🇪 German": "de", "🇫🇷 French": "fr",
        "🇪🇸 Spanish": "es", "🇮🇹 Italian": "it", "🇷🇺 Russian": "ru", "🇨🇳 Chinese": "zh",
        "🇯🇵 Japanese": "ja", "🇰🇷 Korean": "ko", "🇸🇦 Arabic": "ar", "🇵🇹 Portuguese": "pt",
        "🇳🇱 Dutch": "nl", "🇸🇪 Swedish": "sv", "🇵🇱 Polish": "pl", "🇨🇿 Czech": "cs"
    }
    
    # Create the interface with modern theme
    with gr.Blocks(
        title="🤖 AI Assistant Pro", 
        theme=gr.themes.Soft(
            primary_hue=gr.themes.colors.purple,
            secondary_hue=gr.themes.colors.pink,
            neutral_hue=gr.themes.colors.slate
        )
    ) as interface:
        
        # Modern header
        gr.HTML("""
        <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; color: white;">
            <h1 style="font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🤖 AI Assistant Pro
            </h1>
            <p style="font-size: 1.2em; margin: 10px 0 0 0; opacity: 0.9;">
                Your intelligent companion for multiple AI-powered tasks
            </p>
        </div>
        """)
        
        with gr.Tabs() as tabs:
            
            # Wikipedia Tab with modern design
            with gr.TabItem("🔍 Wikipedia Explorer"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("### 📚 Discover Knowledge from Wikipedia")
                        wiki_query = gr.Textbox(
                            label="🔍 What would you like to explore?",
                            placeholder="Try: 'quantum computing', 'space exploration', 'artificial intelligence'...",
                            lines=2
                        )
                        
                        with gr.Row():
                            wiki_results = gr.Slider(
                                label="📊 Number of Results",
                                minimum=1,
                                maximum=10,
                                value=3,
                                step=1
                            )
                            wiki_button = gr.Button(
                                "🚀 Explore Wikipedia", 
                                variant="primary",
                                size="lg"
                            )
                    
                    with gr.Column(scale=1):
                        wiki_status = gr.Textbox(
                            label="Status",
                            interactive=False
                        )
                
                wiki_output = gr.Markdown(label="📖 Discovery Results")
                
                # Examples
                gr.Examples(
                    examples=[
                        ["artificial intelligence", 3],
                        ["quantum physics", 2],
                        ["renewable energy", 4],
                        ["space exploration", 3]
                    ],
                    inputs=[wiki_query, wiki_results]
                )
            
            # Translation Tab with enhanced UI
            with gr.TabItem("🌐 Universal Translator"):
                gr.Markdown("### 🗣️ Break language barriers instantly")
                
                with gr.Row():
                    with gr.Column():
                        translate_text = gr.Textbox(
                            label="✍️ Enter your text",
                            placeholder="Type anything you want to translate...",
                            lines=6
                        )
                        
                        with gr.Row():
                            source_lang = gr.Dropdown(
                                label="🔤 From Language",
                                choices=["🤖 Auto-detect"] + list(languages.keys()),
                                value="🤖 Auto-detect"
                            )
                            target_lang = gr.Dropdown(
                                label="🎯 To Language",
                                choices=list(languages.keys()),
                                value="🇺🇸 English"
                            )
                        
                        with gr.Row():
                            translate_button = gr.Button(
                                "🌟 Translate Magic", 
                                variant="primary",
                                size="lg"
                            )
                            detect_button = gr.Button(
                                "🔍 Detect Language",
                                variant="secondary"
                            )
                    
                    with gr.Column():
                        translate_status = gr.Textbox(
                            label="Status",
                            interactive=False
                        )
                        translate_output = gr.Markdown(
                            label="✨ Translation Result"
                        )
                
                # Translation examples
                gr.Examples(
                    examples=[
                        ["Hello, how are you today?", "🇹🇷 Turkish"],
                        ["Bonjour le monde", "🇺🇸 English"],
                        ["こんにちは世界", "🇺🇸 English"]
                    ],
                    inputs=[translate_text, target_lang]
                )
            
            # Document Processing Tab
            with gr.TabItem("📄 Document Intelligence"):
                gr.Markdown("### 📋 Extract insights from your documents")
                
                with gr.Row():
                    with gr.Column():
                        doc_file = gr.File(
                            label="📎 Drop your document here",
                            file_types=[".pdf", ".doc", ".docx", ".txt", ".md"]
                        )
                        doc_button = gr.Button(
                            "🔬 Analyze Document", 
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        doc_status = gr.Textbox(
                            label="Processing Status",
                            interactive=False
                        )
                
                doc_output = gr.Markdown(label="📊 Document Analysis")
            
            # Image Analysis Tab
            with gr.TabItem("🖼️ Vision AI"):
                gr.Markdown("### 👁️ Unlock the secrets in your images")
                
                with gr.Row():
                    with gr.Column():
                        image_file = gr.Image(
                            label="📸 Upload your image",
                            type="filepath"
                        )
                        image_button = gr.Button(
                            "🎨 Analyze Image", 
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        image_status = gr.Textbox(
                            label="Analysis Status",
                            interactive=False
                        )
                        image_output = gr.Markdown(label="🔍 Vision Results")
            
            # Video Analysis Tab
            with gr.TabItem("🎥 Video Intelligence"):
                gr.Markdown("### 🎬 Decode your videos with AI precision")
                
                with gr.Row():
                    with gr.Column():
                        video_file = gr.Video(label="🎞️ Upload your video")
                        video_button = gr.Button(
                            "🎯 Analyze Video", 
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        video_status = gr.Textbox(
                            label="Processing Status",
                            interactive=False
                        )
                        video_output = gr.Markdown(label="📺 Video Analysis")
        
        # Enhanced footer
        gr.HTML("""
        <div style="margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; text-align: center; color: white;">
            <h3 style="margin-bottom: 20px;">💡 Pro Tips</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 15px;">
                    <strong>🔍 Search:</strong> Use specific keywords for better Wikipedia results
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 15px;">
                    <strong>🌐 Translate:</strong> Auto-detect works great for unknown languages
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 15px;">
                    <strong>📄 Documents:</strong> PDF, DOC, DOCX, TXT, MD supported
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 15px;">
                    <strong>🎥 Media:</strong> Upload images and videos up to 100MB
                </div>
            </div>
            <p style="opacity: 0.8; margin-top: 20px;">
                Powered by AI • Built with ❤️ • Version 2.0
            </p>
        </div>
        """)
        
        # Event handlers with status updates
        def translate_wrapper(text, source, target):
            source_code = "auto" if "Auto-detect" in source else languages.get(source, "auto")
            target_code = languages.get(target, "en")
            status, result = assistant.translate_text(text, target_code, source_code)
            return status, result
        
        def search_wrapper(query, max_results):
            status, result = assistant.search_wikipedia(query, max_results)
            return status, result
        
        def doc_wrapper(file):
            if file is None:
                return "❌ Error", "Please upload a file"
            status, result = assistant.process_document(file)
            return status, result
        
        def image_wrapper(image):
            if image is None:
                return "❌ Error", "Please upload an image"
            status, result = assistant.analyze_image(image)
            return status, result
        
        def video_wrapper(video):
            if video is None:
                return "❌ Error", "Please upload a video"
            status, result = assistant.analyze_video(video)
            return status, result
        
        # Connect events
        wiki_button.click(
            search_wrapper,
            inputs=[wiki_query, wiki_results],
            outputs=[wiki_status, wiki_output]
        )
        
        translate_button.click(
            translate_wrapper,
            inputs=[translate_text, source_lang, target_lang],
            outputs=[translate_status, translate_output]
        )
        
        detect_button.click(
            assistant.detect_language,
            inputs=translate_text,
            outputs=[translate_status, translate_output]
        )
        
        doc_button.click(
            doc_wrapper,
            inputs=doc_file,
            outputs=[doc_status, doc_output]
        )
        
        image_button.click(
            image_wrapper,
            inputs=image_file,
            outputs=[image_status, image_output]
        )
        
        video_button.click(
            video_wrapper,
            inputs=video_file,
            outputs=[video_status, video_output]
        )
    
    return interface

if __name__ == "__main__":
    print("🚀 Starting AI Assistant Pro...")
    print("🔧 Initializing modules...")
    
    # Create and launch the interface
    try:
        interface = create_gradio_interface()
        print("✅ Interface created successfully!")
        print("🌐 Launching web application...")
        print("📱 Access your AI Assistant at: http://localhost:7860")
        print("🔗 For public access, set share=True in the launch() method")
        print("-" * 60)
        
        # Launch with enhanced settings
        interface.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,
            share=False,  # Set to True for public ngrok link
            debug=True,
            show_error=True,
            quiet=False,
            inbrowser=True  # Automatically open browser
        )
        
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("💡 Try installing missing dependencies or check module status")
        print("🔍 Run 'python test_modules.py' to check module status")