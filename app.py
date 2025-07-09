import os
import tempfile
import streamlit as st
from utils.downloader import download_youtube_video
from utils.audio_extractor import extract_audio
from utils.transcriber import transcribe_audio
from utils.chunker import chunk_text
from utils.blog_generator import generate_blog

# Initialize session state
if 'blog_content' not in st.session_state:
    st.session_state.blog_content = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'chunks' not in st.session_state:
    st.session_state.chunks = None

# App UI
st.set_page_config(page_title="AutoBlog AI", page_icon="📹")
st.title("📹 AutoBlog AI")
st.subheader("Transform Videos into Blog Posts")

# Debug mode checkbox
debug_mode = st.sidebar.checkbox("Debug Mode")

# Input options
input_method = st.radio("Input Method:", ("YouTube URL", "Upload MP4 File"))

video_path = None
if input_method == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL:")
    if youtube_url:
        try:
            with st.spinner("Downloading video..."):
                video_path = download_youtube_video(youtube_url)
                if debug_mode:
                    st.sidebar.success(f"Video downloaded to: {video_path}")
        except Exception as e:
            st.error(f"Failed to download video: {str(e)}")
else:
    uploaded_file = st.file_uploader("Upload MP4 File", type=["mp4"])
    if uploaded_file:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(uploaded_file.getvalue())
                video_path = tmp.name
                if debug_mode:
                    st.sidebar.success(f"File saved to: {video_path}")
        except Exception as e:
            st.error(f"Failed to save file: {str(e)}")

# Processing pipeline
if video_path:
    try:
        # Extract audio
        with st.spinner("Extracting audio..."):
            audio_path = extract_audio(video_path)
            if debug_mode:
                st.sidebar.info(f"Audio extracted to: {audio_path}")
        
        # Transcribe audio
        with st.spinner("Transcribing content..."):
            st.session_state.transcript = transcribe_audio(audio_path)
            if debug_mode:
                st.sidebar.text_area("Transcript", st.session_state.transcript, height=200)
        
        # Chunk transcript
        with st.spinner("Processing content..."):
            st.session_state.chunks = chunk_text(st.session_state.transcript)
            if debug_mode:
                st.sidebar.write(f"Created {len(st.session_state.chunks)} chunks")
        
        # Generate blog
        with st.spinner("🧠 Generating blog content..."):
            st.session_state.blog_content = generate_blog(st.session_state.chunks)
        
        # Cleanup
        os.unlink(video_path)
        os.unlink(audio_path)
        
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        if debug_mode:
            st.sidebar.exception(e)

# Display results
if st.session_state.blog_content:
    st.subheader("Generated Blog Post")
    st.markdown(st.session_state.blog_content)
    
    # Download button
    st.download_button(
        label="📥 Download Blog",
        data=st.session_state.blog_content,
        file_name="autoblog.md",
        mime="text/markdown"
    )
    
    # Regeneration button
    if st.button("🔁 Regenerate with Different Style"):
        with st.spinner("🧠 Re-generating blog content..."):
            st.session_state.blog_content = generate_blog(
                st.session_state.chunks, 
                temperature=0.7  # More creative
            )
        st.experimental_rerun()

# Sidebar info
st.sidebar.header("About")
st.sidebar.markdown("""
This tool converts videos to blogs using:
- YouTube/MP4 input
- Whisper for transcription
- GPT-4 for content generation
""")

# Debug info
if debug_mode and st.session_state.transcript:
    with st.sidebar.expander("Debug Info"):
        st.write("Transcript length:", len(st.session_state.transcript))
        st.write("Number of chunks:", len(st.session_state.chunks))
        st.text_area("First Chunk", st.session_state.chunks[0], height=200)