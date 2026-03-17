from scenedetect import detect, ContentDetector
from pathlib import Path

class SceneDetector:
    def detect_scenes(self, video_path: str) -> list:
        """
        Detects scenes in a video using content-based detection.
        Returns a list of tuples containing (start_time, end_time) in seconds.
        """
        print(f"Detecting scenes for: {video_path}")
        scene_list = detect(video_path, ContentDetector())
        
        scenes = []
        for i, scene in enumerate(scene_list):
            start_time = scene[0].get_seconds()
            end_time = scene[1].get_seconds()
            scenes.append({
                "scene_id": i + 1,
                "start": start_time,
                "end": end_time,
                "duration": end_time - start_time
            })
            
        return scenes

if __name__ == "__main__":
    print("Scene detector initialized.")
