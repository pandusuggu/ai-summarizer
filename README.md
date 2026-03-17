# AI Video Summarizer

A production-ready video analysis pipeline that generates meaningful summaries using computer vision, speech recognition, and LLMs.

## Features
- **Smart Input**: Supports local MP4/AVI/MOV and YouTube URLs.
- **Scene Detection**: Intelligent splitting of video into logical segments.
- **Object Recognition**: Identifies key visual elements using YOLOv8.
- **Speech Transcription**: Full transcript generation via OpenAI Whisper.
- **AI Synthesis**: Generates a professional summary report using Gemini or GPT-4o.
- **Premium UI**: Modern dark-mode interface with glassmorphism and real-time progress.

## Tech Stack
- **Backend**: FastAPI, Python
- **ML/CV**: OpenCV, PySceneDetect, Ultralytics YOLOv8, OpenAI Whisper
- **LLM**: Google Gemini / OpenAI GPT-4o
- **Frontend**: Vanilla HTML5, CSS3, JavaScript

## Installation

### Prerequisites
- Python 3.9+
- FFmpeg installed and in your system PATH.

### Steps
1. **Clone/Download** the project.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Rename `.env.example` to `.env`.
   - Add your `GOOGLE_API_KEY` (Gemini) or `OPENAI_API_KEY`.
4. **Run the Server**:
   ```bash
   python api_server.py
   ```
5. **Open the UI**:
   - Open `ui/index.html` in your browser.

## Project Structure
- `api_server.py`: The FastAPI backend.
- `video_pipeline/`: Core logic for each processing step.
- `ui/`: Frontend assets.
- `outputs/`: Where videos, frames, and summaries are stored.
- `models/`: Local cache for ML models.

## Usage
- **Upload**: Drag a video file into the browser.
- **URL**: Paste a YouTube link and click "Analyze".
- **Monitor**: Watch the real-time progress bar as the AI works.
- **Summary**: Read the detailed AI-generated report once complete.
