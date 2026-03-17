from ultralytics import YOLO
import os
from pathlib import Path

class ObjectDetector:
    def __init__(self, model_name="yolov8n.pt"):
        # This will download the model to the current directory or models folder
        self.model = YOLO(model_name)

    def detect_objects(self, frame_paths: list, confidence: float = 0.5) -> list:
        """
        Runs YOLOv8 on a list of frames.
        Returns a list of detections for each frame.
        """
        results_list = []
        
        # Process frames in batches if needed, but for now, simple loop
        for frame_info in frame_paths:
            path = frame_info["path"]
            
            # Check if frame file exists
            if not os.path.exists(path):
                print(f"Frame file not found: {path}")
                continue
                
            try:
                results = self.model(path, conf=confidence, verbose=False)
                
                frame_detections = []
                for r in results:
                    if r.boxes is not None and len(r.boxes) > 0:
                        for box in r.boxes:
                            cls_id = int(box.cls[0])
                            label = self.model.names[cls_id]
                            conf = float(box.conf[0])
                            frame_detections.append({
                                "label": label,
                                "confidence": conf
                            })
                
                # Group by label to find prominent objects
                counts = {}
                for d in frame_detections:
                    counts[d["label"]] = counts.get(d["label"], 0) + 1
                    
                results_list.append({
                    "timestamp": frame_info["timestamp"],
                    "path": path,
                    "counts": counts
                })
                
            except Exception as e:
                print(f"Error processing frame {path}: {e}")
                results_list.append({
                    "timestamp": frame_info["timestamp"],
                    "path": path,
                    "counts": {},
                    "error": str(e)
                })
                
        return results_list

if __name__ == "__main__":
    print("Object detector initialized.")
