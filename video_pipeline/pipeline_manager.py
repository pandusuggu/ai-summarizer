import json
import os
from pathlib import Path
from datetime import datetime

from .video_loader import VideoLoader
from .frame_extractor import FrameExtractor
from .scene_detector import SceneDetector
from .object_detector import ObjectDetector
from .audio_extractor import AudioExtractor
from .speech_to_text import SpeechToText
from .embedding_engine import EmbeddingEngine
from .summarizer import AISummarizer

class VideoPipeline:
    def __init__(self, output_base="outputs"):
        self.output_base = Path(output_base)
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # Initialize modules
        self.loader = VideoLoader(output_dir=self.output_base / "raw")
        self.frame_extractor = FrameExtractor(output_dir=self.output_base / "frames")
        self.scene_detector = SceneDetector()
        self.object_detector = ObjectDetector()
        self.audio_extractor = AudioExtractor(output_dir=self.output_base / "audio")
        self.stt = SpeechToText()
        self.embedder = EmbeddingEngine()
        self.summarizer = AISummarizer()

    def process(self, source: str, video_id: str, status_callback=None) -> dict:
        """Runs the full pipeline on a video source."""
        results = {
            "video_id": video_id,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "status": "Starting..."
        }
        
        def update_status(msg):
            print(f"[{video_id}] {msg}")
            if status_callback:
                status_callback(msg)
            results["status_msg"] = msg

        try:
            # 1. Load/Download
            update_status("Downloading/Loading video...")
            print(f"[DEBUG] Starting video load for: {source}")
            video_path = self.loader.load_video(source)
            print(f"[DEBUG] Video loaded successfully: {video_path}")
            results["video_path"] = video_path
            
            # 2. Scene Detection
            update_status("Detecting scenes...")
            print(f"[DEBUG] Starting scene detection...")
            scenes = self.scene_detector.detect_scenes(video_path)
            print(f"[DEBUG] Scene detection completed: {len(scenes)} scenes")
            results["scenes"] = scenes
            
            # 3. Frame Extraction
            update_status("Extracting and sampling frames...")
            print(f"[DEBUG] Starting frame extraction...")
            frames = self.frame_extractor.extract_frames(video_path, frames_per_second=5, max_frames=30)
            print(f"[DEBUG] Frame extraction completed: {len(frames)} frames")
            results["frames"] = frames
            
            # 4. Object Detection
            update_status(f"Running YOLOv8 Object Detection on {len(frames)} frames...")
            print(f"[DEBUG] Starting object detection...")
            objects = self.object_detector.detect_objects(frames)
            print(f"[DEBUG] Object detection completed")
            results["objects"] = objects
            
            # 5. Audio Extraction
            update_status("Extracting audio stream...")
            print(f"[DEBUG] Starting audio extraction...")
            audio_path = self.audio_extractor.extract_audio(video_path)
            print(f"[DEBUG] Audio extraction completed: {audio_path}")
            results["audio_path"] = audio_path
            
            # 6. Speech-to-Text
            update_status("Transcribing speech (Whisper AI)...")
            print(f"[DEBUG] Starting speech transcription...")
            transcript = self.stt.transcribe(audio_path)
            print(f"[DEBUG] Transcription completed, text length: {len(transcript.get('text', ''))}")
            results["transcript"] = transcript
            
            # 7. AI Summary
            update_status("Generating final AI summary report...")
            print(f"[DEBUG] Starting AI summary generation...")
            summary = self.summarizer.generate_summary(results)
            print(f"[DEBUG] Summary generation completed, length: {len(summary)}")
            results["summary_text"] = summary
            
            results["status"] = "completed"
            update_status("Analysis Complete!")
            
            # Save results to JSON
            result_file = self.output_base / f"results_{video_id}.json"
            with open(result_file, "w") as f:
                json.dump(results, f, indent=4)
            
            results["result_file"] = str(result_file.absolute())
            return results
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            print(f"[{video_id}] Pipeline failed: {e}")
            return results

if __name__ == "__main__":
    print("Video pipeline manager ready.")
