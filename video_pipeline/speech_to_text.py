import whisper
import os
from pathlib import Path

class SpeechToText:
    def __init__(self, model_name="base"):
        # This will download the model weights (e.g., base, small, medium, large-v3)
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribes audio using OpenAI Whisper.
        Returns a dictionary with full text and segmented timestamps.
        """
        if not audio_path or not os.path.exists(audio_path):
            print(f"No audio file to transcribe at: {audio_path}")
            return {"text": "[No audio detected in video]", "segments": []}
            
        print(f"Transcribing audio: {audio_path}")
        result = self.model.transcribe(audio_path, verbose=False)
        
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            })
            
        return {
            "text": result["text"].strip(),
            "segments": segments
        }

if __name__ == "__main__":
    print("Speech to text initialized.")
