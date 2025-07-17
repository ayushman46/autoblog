import whisper
from typing import Tuple, Optional

def transcribe_audio(audio_path: str) -> Tuple[str, dict]:
    """
    Transcribe audio file and return both text and metadata
    
    Args:
        audio_path: Path to audio file (WAV/MP3)
        
    Returns:
        Tuple of (transcribed_text, metadata_dict)
    """
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        
        metadata = {
            "duration": result.get('segments', [{}])[-1].get('end', 0),
            "language": result.get('language', 'en'),
            "model": "base"
        }
        
        return result.get('text', ''), metadata
        
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")