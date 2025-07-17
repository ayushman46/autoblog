import torch
if not hasattr(torch.classes, '__path__'):
    torch.classes.__path__ = []  # Workaround for Streamlit

import os
import tempfile
import streamlit as st
from datetime import datetime
from utils.downloader import download_youtube_video
from utils.audio_extractor import extract_audio
from utils.transcriber import transcribe_audio
from utils.chunker import chunk_text
from utils.blog_generator import generate_blog
from utils.code_extractor import VideoCodeExtractor
import time

# Initialize session state
if 'blog_data' not in st.session_state:
    st.session_state.blog_data = None
if 'processing_steps' not in st.session_state:
    st.session_state.processing_steps = []
if 'extracted_code' not in st.session_state:
    st.session_state.extracted_code = []
if 'video_metadata' not in st.session_state:
    st.session_state.video_metadata = {}

# Page configuration
st.set_page_config(
    page_title="AutoBlog Pro",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    .header {
        color: #2E7D32;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    .step-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #F9F9F9;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.title("📝 AutoBlog Pro")
st.subheader("Transform Tutorial Videos into SEO-Optimized Blog Posts")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    input_method = st.radio("Input Method:", ("YouTube URL", "Upload Video File"))
    
    if input_method == "YouTube URL":
        youtube_url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
        file_path = None
    else:
        uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])
        youtube_url = None
        file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name if uploaded_file else None
        
    # Only keep creativity slider (remove other options)
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.3, 0.05,
                          help="Higher values = more creative but less predictable output")
    
    debug_mode = st.checkbox("Enable Debug Mode", value=False)
        
    process_btn = st.button("Generate Blog", type="primary", use_container_width=True)

# Processing pipeline
def log_step(step, message):
    """Log processing step with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.processing_steps.append(f"{timestamp} - {step}: {message}")
    return f"✅ {step} completed"

if process_btn and (youtube_url or uploaded_file):
    try:
        # Start processing pipeline
        start_time = time.time()
        progress_bar = st.progress(0)
        status_area = st.empty()
        
        # Step 1: Get video file
        if youtube_url:
            status_area.markdown("### 🔄 Step 1/7: Downloading YouTube video...")
            video_path = download_youtube_video(youtube_url)
            st.session_state.video_metadata['source'] = "youtube"
            st.session_state.video_metadata['url'] = youtube_url
            log_step("Download", f"Downloaded YouTube video to {video_path}")
        else:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            video_path = file_path
            st.session_state.video_metadata['source'] = "upload"
            st.session_state.video_metadata['filename'] = uploaded_file.name
            log_step("Upload", f"Saved uploaded file to {file_path}")
            
        progress_bar.progress(10)
        
        # Step 2: Extract audio
        status_area.markdown("### 🔄 Step 2/7: Extracting audio from video...")
        audio_path = extract_audio(video_path)
        log_step("Audio Extraction", f"Extracted audio to {audio_path}")
        progress_bar.progress(20)
        
        # Step 3: Transcribe audio
        status_area.markdown("### 🔄 Step 3/7: Transcribing audio content...")
        transcript, trans_metadata = transcribe_audio(audio_path)
        st.session_state.video_metadata['transcription'] = trans_metadata
        log_step("Transcription", 
                f"Transcribed {trans_metadata['duration']:.1f}s audio with {trans_metadata['model']} model")
        progress_bar.progress(40)
        
        # Step 4: Chunk transcript
        status_area.markdown("### 🔄 Step 4/7: Processing transcript content...")
        chunks = chunk_text(transcript)
        log_step("Chunking", f"Split transcript into {len(chunks)} chunks")
        progress_bar.progress(50)
        
        # Step 5: Extract code from video (using automatic settings)
        status_area.markdown("### 🔄 Step 5/7: Extracting code from video frames...")
        code_extractor = VideoCodeExtractor(video_path)  # No parameters = uses automatic settings
        st.session_state.extracted_code = code_extractor.extract_code()
        
        if debug_mode:
            code_extractor.visualize_extraction("debug_frames")
            
        log_step("Code Extraction", 
                f"Extracted {len(st.session_state.extracted_code)} code snippets from video")
        progress_bar.progress(70)
        
        # Step 6: Generate blog content
        status_area.markdown("### 🔄 Step 6/7: Generating blog post...")
        blog_data = generate_blog(chunks, st.session_state.extracted_code, temperature)
        st.session_state.blog_data = blog_data
        log_step("Blog Generation", 
                f"Generated {blog_data['word_count']} word blog with {blog_data['code_snippets_used']} code snippets")
        progress_bar.progress(90)
        
        # Step 7: Cleanup
        status_area.markdown("### 🔄 Step 7/7: Cleaning up temporary files...")
        for path in [video_path, audio_path]:
            if os.path.exists(path):
                os.remove(path)
        log_step("Cleanup", "Removed temporary files")
        progress_bar.progress(100)
        
        # Finalize
        duration = time.time() - start_time
        status_area.success(f"✅ Processing completed in {duration:.1f} seconds!")
        
    except Exception as e:
        status_area.error(f"❌ Processing failed: {str(e)}")
        if debug_mode:
            st.exception(e)

# Display results
if st.session_state.blog_data:
    st.markdown("---")
    st.subheader("Generated Blog Post")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {st.session_state.blog_data['title']}")
        st.markdown(st.session_state.blog_data['content'])
        
    with col2:
        st.metric("Word Count", st.session_state.blog_data['word_count'])
        st.metric("Code Snippets", st.session_state.blog_data['code_snippets_used'])
        st.text_area("Meta Description", 
                    st.session_state.blog_data['meta_description'],
                    height=100)
        
        if st.session_state.extracted_code:
            with st.expander("Extracted Code Snippets"):
                for i, snippet in enumerate(st.session_state.extracted_code):
                    st.caption(f"Snippet {i+1}")
                    st.code(snippet, language='python')
    
    # Download button
    st.download_button(
        label="Download Blog",
        data=st.session_state.blog_data['content'],
        file_name=f"{st.session_state.blog_data['title'].replace(' ', '_')}.md",
        mime="text/markdown"
    )

# Display processing log
if st.session_state.processing_steps:
    with st.expander("Processing Log"):
        for step in st.session_state.processing_steps:
            st.markdown(f"<div class='step-card'>{step}</div>", unsafe_allow_html=True)

# Instructions
with st.expander("How to Use AutoBlog Pro"):
    st.markdown("""
    **1. Input Source**  
    - Provide either a YouTube URL or upload a video file
    
    **2. Set Creativity Level**  
    - Lower = more factual, Higher = more creative
    
    **3. Generate Blog**  
    - Click the Generate Blog button
    - The system will automatically:
        1. Download/upload video
        2. Extract audio track
        3. Transcribe audio to text
        4. Process transcript
        5. Extract code from video frames (optimized settings)
        6. Generate SEO-optimized blog
        7. Clean up temporary files
    
    **4. Review & Download**  
    - View generated blog content
    - See extracted code snippets
    - Download as Markdown file
    
    **Supported Video Formats**  
    - MP4, MOV, AVI (H.264 codec recommended)
    - Maximum duration: 60 minutes
    """)