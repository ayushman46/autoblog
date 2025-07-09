import yt_dlp
import tempfile
import os

def download_youtube_video(url):
    """Download YouTube video and return local file path"""
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "youtube_video.mp4")
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
