import uuid, subprocess, shutil, threading, textwrap
from pathlib import Path
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw, ImageFont

app = FastAPI(title="AI YouTube Studio")
templates = Jinja2Templates(directory="templates")
OUTPUT = Path("/tmp/ai-youtube-studio")
OUTPUT.mkdir(exist_ok=True)
JOBS = {}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def build(job_id, topic):
    try:
        JOBS[job_id]["status"] = "rendering"
        directory = OUTPUT / job_id
        directory.mkdir(parents=True, exist_ok=True)
        title_font = ImageFont.truetype(FONT, 52)
        body_font = ImageFont.truetype(FONT, 32)
        scenes = [
            (topic, "An introduction to the topic"),
            ("How it works", "Explore the fundamental ideas"),
            ("Why it matters", "Understand practical applications"),
            ("Next steps", "Research, verify, and learn more"),
        ]
        for i, (heading, subtitle) in enumerate(scenes):
            im = Image.new("RGB", (1280, 720), (13+i*8, 25+i*5, 48+i*7))
            draw = ImageDraw.Draw(im)
            draw.rounded_rectangle((80, 130, 1200, 590), radius=35, outline=(75,180,230), width=4)
            for j, line in enumerate(textwrap.wrap(heading, width=32)[:3]):
                draw.text((115, 210+j*70), line, font=title_font, fill="white")
            draw.text((115, 465), subtitle, font=body_font, fill=(165,215,235))
            im.save(directory / f"scene{i}.png")
        concat = directory / "frames.txt"
        concat.write_text("".join(f"file 'scene{i}.png'\nduration 3\n" for i in range(4)) + "file 'scene3.png'\n")
        out = directory / "video.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(concat), "-vf", "fps=24,format=yuv420p",
                        "-c:v", "libx264", "-preset", "ultrafast", "-movflags",
                        "+faststart", str(out)], cwd=directory, check=True, timeout=110)
        JOBS[job_id]["status"] = "ready"
    except Exception as exc:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(exc)[:250]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
def generate(topic: str = Form(...)):
    topic = topic.strip()
    if not 3 <= len(topic) <= 120:
        raise HTTPException(400, "Topic must be 3-120 characters")
    if sum(v["status"] in ("queued", "rendering") for v in JOBS.values()) >= 2:
        raise HTTPException(429, "Render queue is full")
    job_id = uuid.uuid4().hex[:12]
    JOBS[job_id] = {"status": "queued", "topic": topic}
    threading.Thread(target=build, args=(job_id, topic), daemon=True).start()
    return {"job_id": job_id}

@app.get("/api/jobs/{job_id}")
def status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(404, "Job not found")
    return JOBS[job_id]

@app.get("/api/jobs/{job_id}/download")
def download(job_id: str):
    if JOBS.get(job_id, {}).get("status") != "ready":
        raise HTTPException(404, "Video not ready")
    return FileResponse(OUTPUT / job_id / "video.mp4", media_type="video/mp4", filename="youtube-draft.mp4")

@app.get("/health")
def health():
    return {"ok": True, "ffmpeg": bool(shutil.which("ffmpeg"))}
