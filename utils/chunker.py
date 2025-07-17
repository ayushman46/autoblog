from typing import List, Tuple
import re
import nltk
from nltk.tokenize import sent_tokenize
import os

# Ensure NLTK data is downloaded
def setup_nltk():
    try:
        # Create nltk_data directory if it doesn't exist
        nltk_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
        if not os.path.exists(nltk_dir):
            os.makedirs(nltk_dir)
        
        # Download required data
        nltk.download('punkt', download_dir=nltk_dir, quiet=True)
        nltk.download('punkt_tab', download_dir=nltk_dir, quiet=True)
        
        # Add to NLTK path
        nltk.data.path.append(nltk_dir)
    except Exception as e:
        raise RuntimeError(f"Failed to setup NLTK: {str(e)}")

# Run setup when module loads
setup_nltk()

def chunk_text(transcript: str, max_chunk_size: int = 500) -> List[Tuple[str, int]]:
    """
    Splits transcript into chunks with word counts
    Args:
        transcript: Input text
        max_chunk_size: Max characters per chunk
    Returns:
        List of (text_chunk, word_count)
    """
    if not transcript:
        return []

    # Clean text
    clean_text = re.sub(r'\s+', ' ', transcript).strip()
    chunks = []
    current_chunk = ""
    current_words = 0
    
    try:
        sentences = sent_tokenize(clean_text)
        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)
            
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append((current_chunk.strip(), current_words))
                current_chunk = ""
                current_words = 0
                
            current_chunk += sentence + " "
            current_words += word_count
            
        if current_chunk:
            chunks.append((current_chunk.strip(), current_words))
            
    except Exception as e:
        raise RuntimeError(f"Chunking failed: {str(e)}")
    
    return chunks