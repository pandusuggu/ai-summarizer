from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class AISummarizer:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        
        if self.groq_key:
            self.groq_client = Groq(api_key=self.groq_key)
        else:
            print("Warning: Groq API key not configured.")

    def generate_summary(self, metadata: dict) -> str:
        """
        Synthesizes video metadata into a structured summary.
        metadata: {
            "video_info": {...},
            "scenes": [...],
            "objects": [...],
            "transcript": {...}
        }
        """
        print(f"[SUMMARIZER] Processing metadata with {len(metadata.get('scenes', []))} scenes")
        print(f"[SUMMARIZER] Objects detected: {len(metadata.get('objects', []))}")
        transcript_text = metadata.get('transcript', {}).get('text', '')
        print(f"[SUMMARIZER] Transcript length: {len(transcript_text)} characters")
        print(f"[SUMMARIZER] Transcript preview: {transcript_text[:200]}...")
        
        prompt = self._build_prompt(metadata)
        
        if self.groq_key:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Groq API Error: {e}")
                return f"AI Summary generation failed: {str(e)}"
        else:
            return "AI Summary generation failed: Groq API key not configured."

    def _build_prompt(self, metadata: dict) -> str:
        # Handle missing or empty data gracefully
        scenes = metadata.get('scenes', [])
        objects = metadata.get('objects', [])
        transcript = metadata.get('transcript', {})
        
        scenes_str = "\n".join([f"Scene {s.get('scene_id', s.get('id', '?'))} ({s.get('start', 0):.2f}s - {s.get('end', 0):.2f}s)" for s in scenes[:20]]) if scenes else "No scene data available"
        
        # Aggregate top objects
        all_objects = {}
        for obj_info in objects:
            counts = obj_info.get('counts', {})
            for label, count in counts.items():
                all_objects[label] = all_objects.get(label, 0) + count
        
        top_objects = sorted(all_objects.items(), key=lambda x: x[1], reverse=True)[:10]
        objects_str = ", ".join([f"{k} ({v})" for k, v in top_objects]) if top_objects else "No objects detected"
        
        transcript_text = transcript.get('text', '') if transcript else ''
        if not transcript_text:
            transcript_text = "No speech detected in the video"
        
        prompt = f"""
You are an expert video content analyst. Your task is to provide an accurate and detailed summary based on the video analysis data below.

CRITICAL INSTRUCTIONS:
- Be FACTUALLY ACCURATE based only on the provided data
- Do NOT invent or assume information not present in the transcript or visual data
- Focus on what is actually said and shown in the video
- If the transcript is empty or minimal, state that clearly

VIDEO ANALYSIS DATA:
- Total Scenes Detected: {len(scenes)}
- Duration Analysis: {scenes_str if scenes else "No scene timing data available"}
- Visual Elements Detected: {objects_str}
- Audio Transcript: "{transcript_text[:3000]}"

ANALYSIS REQUIREMENTS:
1. **Content Summary**: Describe what actually happens in the video based on the transcript and visual data
2. **Visual Elements**: List objects/scenes actually detected (from the objects data above)
3. **Key Topics**: Extract main subjects from the spoken content only
4. **Important Details**: Include specific facts, numbers, or statements from the transcript
5. **Accuracy Note**: Mention if transcript quality was poor or missing

IMPORTANT: Base your summary ONLY on the provided transcript and object detection data. Do not hallucinate or add information not present in the source data.

Format with clear Markdown headers.
        """
        return prompt

if __name__ == "__main__":
    print("AI Summarizer initialized.")
