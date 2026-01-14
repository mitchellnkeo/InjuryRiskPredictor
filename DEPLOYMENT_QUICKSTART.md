# Quick Deployment Guide

This is a quick reference for deploying the Injury Risk Predictor app.

## Prerequisites

- Model files must exist: `backend/models/random_forest_model.pkl` and `backend/models/scaler.pkl`
- GitHub repository connected
- Accounts on Railway/Render (backend) and Vercel (frontend)

---

## Backend Deployment (Railway)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. **Settings:**
   - Root Directory: `.` (project root)
   - Dockerfile Path: `backend/Dockerfile`
5. Deploy!
6. Copy the URL (e.g., `https://your-api.up.railway.app`)

**Test:**
```bash
curl https://your-api.up.railway.app/health
```

---

## Backend Deployment (Render)

1. Go to https://render.com
2. New + → Web Service
3. Connect GitHub repository
4. **Settings:**
   - Root Directory: `.`
   - Dockerfile Path: `backend/Dockerfile`
   - Docker Context: `.`
5. Deploy!
6. Copy the URL (e.g., `https://your-api.onrender.com`)

**Test:**
```bash
curl https://your-api.onrender.com/health
```

---

## Frontend Deployment (Vercel)

1. Go to https://vercel.com
2. Add New Project → Import GitHub repo
3. **Settings:**
   - Root Directory: `frontend`
   - Framework: Next.js (auto-detected)
4. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: Your backend URL (from Railway/Render)
5. Deploy!
6. Copy the URL (e.g., `https://your-app.vercel.app`)

**Test:**
- Visit your Vercel URL
- Try the prediction form
- Check browser console for errors

---

## Update CORS (After Frontend Deployment)

Once you have your frontend URL, update `backend/app/main.py`:

```python
cors_origins = [
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add your Vercel URL
]
```

Or set `CORS_ORIGINS` environment variable in Railway/Render:
```
CORS_ORIGINS=https://your-app.vercel.app
```

---

## Test Locally First (Optional)

**Note:** Docker is optional. You can deploy directly to Railway/Render without Docker installed - they build the image for you.

If you want to test locally:

1. **Install Docker Desktop:**
   - Download from https://www.docker.com/products/docker-desktop/
   - Install and start Docker Desktop

2. **Test Docker build:**
   ```bash
   # From project root
   docker build -t injury-api -f backend/Dockerfile .
   docker run -p 8000:8000 -e PORT=8000 injury-api
   ```

**Or skip local testing and deploy directly** - Railway/Render will build the Docker image automatically.

---

## Troubleshooting

- **"No model file found"**: Ensure `backend/models/` has `.pkl` files
- **"ModuleNotFoundError: No module named 'src'"**: Dockerfile should copy `src/` directory
- **CORS errors**: Update CORS origins in `backend/app/main.py`
- **Build fails**: Check deployment logs for specific errors

See `docs/DEPLOYMENT.md` for detailed troubleshooting.
