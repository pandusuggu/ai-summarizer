from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os
import shutil
from pathlib import Path

from video_pipeline.pipeline_manager import VideoPipeline

app = FastAPI(title="AI Video Summarizer API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared state (In-memory for simplicity)
jobs = {}
pipeline = VideoPipeline()

# Serve static files
app.mount("/static", StaticFiles(directory="ui"), name="static")

@app.get("/")
async def root():
    return FileResponse("ui/index.html")

class YouTubeRequest(BaseModel):
    url: str

@app.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    temp_dir = Path("outputs/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = temp_dir / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    jobs[job_id] = {"status": "queued", "source": str(file_path)}
    background_tasks.add_task(run_pipeline_task, job_id, str(file_path))
    
    return {"job_id": job_id, "status": "queued"}

@app.post("/process-youtube")
async def process_youtube(request: YouTubeRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "source": request.url}
    background_tasks.add_task(run_pipeline_task, job_id, request.url)
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/summary/{job_id}")
async def get_summary(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if jobs[job_id]["status"] != "completed":
        return {"status": jobs[job_id]["status"], "message": "Summary not ready yet"}
    
    return jobs[job_id]["results"]

def run_pipeline_task(job_id: str, source: str):
    """Run pipeline task."""
    def update_job_status(msg):
        jobs[job_id]["status_msg"] = msg
        print(f"[{job_id}] {msg}")
    
    jobs[job_id]["status"] = "processing"
    results = pipeline.process(source, job_id, update_job_status)
    jobs[job_id]["status"] = results["status"]
    if results["status"] == "completed":
        jobs[job_id]["results"] = results
    else:
        jobs[job_id]["error"] = results.get("error", "Unknown error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
