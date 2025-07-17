
Convert YouTube videos or local MP4 files into professional blog posts with AI.

## Features
- One-click conversion from video to blog
- Supports YouTube URLs or file uploads
- Preserves original content structure
- Multiple output style options
- Download as Markdown

## Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/AIblog.git
   cd AIblog
Set up environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
Install dependencies:

bash
pip install openai langchain-openai streamlit yt-dlp openai-whisper ffmpeg-python python-dotenv
Install FFmpeg:

bash
# Windows (Admin)
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg
Configure API key:

bash
echo "OPENAI_API_KEY=your_key_here" > .env
Usage
bash
streamlit run app.py
Then:

Paste YouTube URL or upload MP4

Wait for processing

View/download generated blog

Project Structure
text
AIblog/
├── app.py
├── .env
├── requirements.txt
└── utils/
    ├── downloader.py
    ├── audio_extractor.py  
    ├── transcriber.py
    ├── chunker.py
    └── blog_generator.py4

    https://www.youtube.com/watch?v=DLn3jOsNRVE
