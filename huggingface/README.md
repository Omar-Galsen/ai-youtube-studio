---
title: AI YouTube Studio API
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# AI YouTube Studio — Hugging Face Space

A FastAPI + FFmpeg video draft backend for the [Render frontend](https://ai-youtube-studio-n048.onrender.com).

This generates a silent four-scene MP4 draft, **not** AI research or narration yet.

## Deploy
1. Create a new **Docker** Space on Hugging Face, using the free CPU Basic hardware if available.
2. Copy the following GitHub repository files into the Space repository root: `Dockerfile`, `app.py`, `requirements.txt`, `templates/index.html`, and this `README.md`. You can use GitHub import or upload files. The Space must contain the files itself; a GitHub link alone does not deploy it.
3. In Space **Settings → Variables and secrets**, add variable `FRONTEND_ORIGIN` = `https://ai-youtube-studio-n048.onrender.com`.
4. Wait for the Space to build. Check `https://YOUR-SPACE.hf.space/health`.
5. Update GitHub `dist/config.js` with `window.AI_STUDIO_API_URL = "https://YOUR-SPACE.hf.space";` and redeploy the Render Static Site.

## Notes
- Free CPU Spaces may sleep and have limited resources. Videos and jobs are temporary.
- The current API is unauthenticated. Avoid broad public promotion until authentication and rate limiting are added.
- Generated files are stored in `/tmp` and will disappear on restart.
