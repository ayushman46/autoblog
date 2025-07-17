import cv2
import numpy as np
import pytesseract
import os
import re
from typing import List, Optional

class VideoCodeExtractor:
    """Extracts code snippets from video frames using OCR"""
    
    def __init__(self, video_path: str, interval: int = 10, min_confidence: float = 0.7):
        """
        Initialize the code extractor
        
        Args:
            video_path: Path to video file
            interval: Seconds between frame captures
            min_confidence: Minimum OCR confidence (0-1)
        """
        self.video_path = video_path
        self.interval = interval
        self.min_confidence = min_confidence
        self.code_snippets = set()
        
        # Configure Tesseract (update path as needed)
        self.tesseract_config = r'--oem 3 --psm 6'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def _preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Enhance frame for better OCR results"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.medianBlur(thresh, 3)

    def _is_valid_code(self, text: str) -> bool:
        """Check if text appears to be code"""
        code_patterns = [
            r'\b(def|class|import|from|return|if|else|for|while|try|except)\b',
            r'[{}()\[\];=><|&]',
            r'\.\w+\(.*\)'
        ]
        return any(re.search(pattern, text) for pattern in code_patterns)

    def extract_code(self) -> List[str]:
        """Main method to extract code from video"""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError(f"Could not open video: {self.video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                processed = self._preprocess_frame(frame)
                text = pytesseract.image_to_string(
                    processed,
                    config=self.tesseract_config
                ).strip()

                if text and self._is_valid_code(text):
                    self.code_snippets.add(text)

            frame_count += 1

        cap.release()
        return list(self.code_snippets)

# Example usage
if __name__ == "__main__":
    extractor = VideoCodeExtractor("test.mp4")
    print("Extracted code:", extractor.extract_code())