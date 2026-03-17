import cv2
import os
from pathlib import Path

class FrameExtractor:
    def __init__(self, output_dir="outputs/frames"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_frames(self, video_path: str, frames_per_second: int = 5, max_frames: int = 50) -> list:
        """
        Extracts frames from video at specific rate.
        Returns a list of paths to the extracted frames.
        """
        video_name = Path(video_path).stem
        frame_dir = self.output_dir / video_name
        frame_dir.mkdir(parents=True, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30 # Fallback
        
        # Calculate frame interval for desired frames per second
        frame_interval = int(fps / frames_per_second)
        frame_paths = []
        count = 0
        success = True
        
        while count * frame_interval < cap.get(cv2.CAP_PROP_FRAME_COUNT) and count < max_frames:
            # We want to seek specifically
            cap.set(cv2.CAP_PROP_POS_FRAMES, count * frame_interval)
            success, frame = cap.read()
            
            if success:
                timestamp = count / frames_per_second
                frame_filename = f"frame_{count:04d}_ts_{timestamp:.2f}.jpg"
                frame_path = frame_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append({
                    "path": str(frame_path.absolute()),
                    "timestamp": timestamp
                })
                count += 1
            else:
                break
                
        cap.release()
        return frame_paths

if __name__ == "__main__":
    print("Frame extractor initialized.")
