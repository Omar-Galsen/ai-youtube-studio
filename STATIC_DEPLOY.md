# Render split deployment

## 1. Static frontend
Create a Render **Static Site** connected to this repo.
- Branch: main
- Build command: `echo "Static frontend ready"`
- Publish directory: `dist`

## 2. Video API backend
Create a **Web Service** from the same repo.
- Runtime: Docker
- Dockerfile: `./Dockerfile`
- Plan: Free (if available)
- Set environment variable `FRONTEND_ORIGIN` to the exact frontend origin, e.g. `https://ai-youtube-studio.onrender.com` (no trailing slash)

## 3. Connect frontend to backend
Edit `dist/config.js` and set `window.AI_STUDIO_API_URL` to your Web Service URL, e.g. `https://ai-youtube-studio-api.onrender.com`.
Commit the change to GitHub. Render redeploys the Static Site automatically.

## 4. Verify
Open backend `https://YOUR-BACKEND.onrender.com/health` and confirm `{"ok":true,"ffmpeg":true}`.
Then open the frontend and generate a topic. Download the MP4.

## Limitations
This is a silent title-card video draft generator, not an AI narrator.
Render free Web Services sleep on inactivity; initial requests may take time.
Jobs and generated files are ephemeral and disappear when the backend restarts.
The current API has no authentication: avoid sharing the backend publicly until rate limits and authentication are added.
