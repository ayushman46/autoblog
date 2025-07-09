from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def chunk_text(
    text: str,
    chunk_size: int = 3000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split text into manageable chunks for processing.
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum characters per chunk
        chunk_overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(text)

# Test function
if __name__ == "__main__":
    test_text = "Lorem ipsum " * 1000  # Sample long text
    chunks = chunk_text(test_text)
    print(f"Split into {len(chunks)} chunks")
    print("First chunk:", chunks[0][:100] + "...")