import os
import subprocess
import tempfile

def extract_audio(video_path):
    """Extract audio using FFmpeg and return WAV file path"""
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "audio.wav")
    
    try:
        subprocess.run([
            "ffmpeg",
            "-i", video_path,       # Input file
            "-vn",                  # Disable video
            "-ac", "1",            # Mono audio
            "-ar", "16000",        # 16kHz sample rate (optimal for Whisper)
            "-y",                   # Overwrite without asking
            audio_path
        ], check=True, capture_output=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg failed: {e.stderr.decode()}")

# Test function (optional)
if __name__ == "__main__":
    test_path = input("Enter test video path: ")
    print("Extracted audio:", extract_audio(test_path))