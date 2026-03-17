import ffmpeg
import os
from pathlib import Path

class AudioExtractor:
    def __init__(self, output_dir="outputs/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_audio(self, video_path: str) -> str:
        """
        Extracts audio from video file using ffmpeg.
        Returns the path to the audio file or an empty string if no audio is found.
        """
        video_name = Path(video_path).stem
        audio_path = self.output_dir / f"{video_name}.mp3"
        
        if audio_path.exists():
            return str(audio_path.absolute())
            
        try:
            # Check if audio stream exists
            probe = ffmpeg.probe(video_path)
            audio_streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
            
            if not audio_streams:
                print(f"No audio stream found in {video_path}. Creating empty fallback.")
                # Instead of complex lavfi, just create a small dummy file or return empty
                # We'll return an empty string and handle it in the next stage
                return ""

            stream = ffmpeg.input(video_path)
            stream = ffmpeg.output(stream, str(audio_path), acodec='libmp3lame', ac=2, ar='44100')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return str(audio_path.absolute())
        except Exception as e:
            print(f"Audio extraction warning for {video_path}: {e}")
            return ""

if __name__ == "__main__":
    print("Audio extractor initialized.")
