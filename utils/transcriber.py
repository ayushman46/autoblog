import os
import whisper
from typing import Optional

def transcribe_audio(
    audio_path: str,
    model_size: str = "base",
    language: Optional[str] = None
) -> str:
    """
    Transcribe audio using Whisper.
    
    Args:
        audio_path: Path to audio file (WAV/MP3)
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Optional language code (e.g., 'en')
    
    Returns:
        Transcribed text
    """
    try:
        # Load model (will auto-download on first run)
        model = whisper.load_model(model_size)
        
        # Run transcription
        result = model.transcribe(
            audio_path,
            language=language,
            fp16=False  # Disable GPU for better compatibility
        )
        
        return result["text"]
    
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")

# Test the function directly if needed
if __name__ == "__main__":
    test_file = input("Enter audio file path: ")
    print("Transcription:", transcribe_audio(test_file))