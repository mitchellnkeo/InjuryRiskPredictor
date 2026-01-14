# Deployment Guide

This guide covers deploying both the backend API and frontend application.

---

## Table of Contents

1. [Backend Deployment (Railway/Render)](#backend-deployment)
2. [Frontend Deployment (Vercel)](#frontend-deployment)
3. [Environment Variables](#environment-variables)
4. [Troubleshooting](#troubleshooting)

---

## Backend Deployment

### Option 1: Railway

#### Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub repository connected

#### Steps

1. **Create New Project**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Service**
   - Railway will auto-detect the Dockerfile
   - **Important:** Set root directory to project root (not `backend/`)
   - Set Dockerfile path: `backend/Dockerfile`
   - Docker build context should be project root

3. **Set Environment Variables**
   - `ENVIRONMENT=production` (optional)
   - Railway will automatically set `PORT` variable

4. **Deploy**
   - Railway will build and deploy automatically
   - Check logs for any errors
   - Copy the generated URL (e.g., `https://your-api.up.railway.app`)

5. **Verify Deployment**
   ```bash
   # Health check
   curl https://your-api.up.railway.app/health
   
   # API docs
   # Visit: https://your-api.up.railway.app/docs
   ```

#### Railway-Specific Notes
- Railway uses `$PORT` environment variable automatically
- Dockerfile handles this with `${PORT:-8000}` fallback
- No need to manually set PORT in Railway

---

### Option 2: Render

#### Prerequisites
- Render account (sign up at https://render.com)
- GitHub repository connected

#### Steps

1. **Create New Web Service**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name:** `injury-risk-api` (or your choice)
   - **Region:** Choose closest to your users
   - **Branch:** `main` (or your default branch)
   - **Root Directory:** `.` (project root)
   - **Environment:** `Docker`
   - **Dockerfile Path:** `backend/Dockerfile`
   - **Docker Context:** `.` (project root)

3. **Set Environment Variables**
   - `ENVIRONMENT=production` (optional)
   - Render will automatically set `PORT` variable

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy
   - Check build logs for errors
   - Copy the generated URL (e.g., `https://your-api.onrender.com`)

5. **Verify Deployment**
   ```bash
   # Health check
   curl https://your-api.onrender.com/health
   
   # API docs
   # Visit: https://your-api.onrender.com/docs
   ```

#### Render-Specific Notes
- Render uses `$PORT` environment variable automatically
- Free tier services spin down after inactivity (cold starts)
- Consider upgrading to paid tier for production

---

### Testing Docker Build Locally (Optional)

**Note:** Docker is optional for local testing. You can deploy directly to Railway/Render without Docker installed locally - they will build the Docker image for you.

If you want to test the Docker build locally first:

#### Install Docker Desktop (macOS)

1. **Download Docker Desktop:**
   - Visit https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Mac (Apple Silicon or Intel)
   - Install the `.dmg` file

2. **Start Docker Desktop:**
   - Open Docker Desktop from Applications
   - Wait for it to start (whale icon in menu bar)
   - Verify installation:
     ```bash
     docker --version
     ```

3. **Test Docker Build:**
   ```bash
   # Build the image (from project root)
   docker build -t injury-api -f backend/Dockerfile .

   # Run the container
   docker run -p 8000:8000 -e PORT=8000 injury-api

   # Test health endpoint (in another terminal)
   curl http://localhost:8000/health
   ```

**Note:** The Dockerfile expects to be built from the project root, not from the `backend/` directory. This is because it needs access to both `backend/` and `src/` directories.

**Note:** Make sure you have model files (`random_forest_model.pkl` and `scaler.pkl`) in `backend/models/` before building.

#### Skip Local Testing

If you don't want to install Docker locally, you can:
1. Deploy directly to Railway/Render
2. They will build the Docker image automatically
3. Check deployment logs for any build errors
4. Test the deployed API instead

---

## Frontend Deployment

### Vercel

#### Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub repository connected

#### Steps

1. **Import Project**
   - Go to Vercel dashboard
   - Click "Add New..." → "Project"
   - Import your GitHub repository

2. **Configure Project**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)

3. **Set Environment Variables**
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
     - Example: `https://your-api.up.railway.app`
     - Or: `https://your-api.onrender.com`
   - **Important:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically
   - Check build logs for errors
   - Copy the generated URL (e.g., `https://your-app.vercel.app`)

5. **Verify Deployment**
   - Visit your Vercel URL
   - Test the prediction form
   - Check browser console for errors
   - Verify API calls are working

#### Vercel-Specific Notes
- Automatic HTTPS
- Global CDN
- Preview deployments for each PR
- Custom domains supported

---

## Environment Variables

### Backend

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PORT` | Server port | No | `8000` |
| `ENVIRONMENT` | Environment name | No | `development` |

**Note:** `PORT` is automatically set by Railway/Render. Don't manually set it unless deploying elsewhere.

### Frontend

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes | `http://localhost:8000` |

**Note:** `NEXT_PUBLIC_` prefix is required for client-side access in Next.js.

---

## Troubleshooting

### Backend Issues

#### Issue: "No model file found"
**Solution:** Ensure `backend/models/` contains:
- `random_forest_model.pkl` (or `*_model.pkl`)
- `scaler.pkl`

#### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution:** Ensure Dockerfile copies `src/` directory:
```dockerfile
COPY src/ ./src/
```

#### Issue: "Port already in use"
**Solution:** Railway/Render sets `PORT` automatically. Don't hardcode port in code.

#### Issue: "CORS errors"
**Solution:** Update CORS origins in `backend/app/main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend.vercel.app",  # Add your frontend URL
]
```

### Frontend Issues

#### Issue: "API calls failing"
**Solution:** 
1. Check `NEXT_PUBLIC_API_URL` is set correctly
2. Verify backend is running and accessible
3. Check CORS settings in backend
4. Check browser console for errors

#### Issue: "Build fails"
**Solution:**
1. Check for TypeScript errors: `npm run build`
2. Ensure all dependencies are in `package.json`
3. Check Node.js version (Vercel uses Node 18+)

#### Issue: "Environment variables not working"
**Solution:**
- Variables must be prefixed with `NEXT_PUBLIC_` for client-side access
- Redeploy after changing environment variables
- Check Vercel dashboard → Settings → Environment Variables

---

## Deployment Checklist

### Before Deploying Backend
- [ ] Model files exist in `backend/models/`
- [ ] Dockerfile builds successfully locally
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible at `/docs`
- [ ] Test prediction endpoint works

### Before Deploying Frontend
- [ ] Backend is deployed and accessible
- [ ] `NEXT_PUBLIC_API_URL` is set correctly
- [ ] `npm run build` succeeds locally
- [ ] No TypeScript errors
- [ ] All components render correctly

### After Deployment
- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] Prediction form submits successfully
- [ ] Results page displays correctly
- [ ] No console errors in browser
- [ ] CORS is configured correctly

---

## Production Considerations

### Backend
- **Model Versioning:** Consider versioning models (e.g., `v1_model.pkl`)
- **Logging:** Set up proper logging (Railway/Render provide logs)
- **Monitoring:** Consider adding health check monitoring
- **Rate Limiting:** Add rate limiting for production
- **Security:** Review CORS settings, add authentication if needed

### Frontend
- **Error Boundaries:** Add React error boundaries
- **Analytics:** Consider adding analytics (Vercel Analytics, Google Analytics)
- **Performance:** Monitor Core Web Vitals
- **SEO:** Add proper meta tags, Open Graph tags
- **Accessibility:** Ensure WCAG compliance

---

## Quick Reference

### Backend URLs
- **Health:** `https://your-api.up.railway.app/health`
- **Docs:** `https://your-api.up.railway.app/docs`
- **Predict:** `POST https://your-api.up.railway.app/api/predict`

### Frontend URLs
- **Home:** `https://your-app.vercel.app`
- **Predict:** `https://your-app.vercel.app/predict`
- **Results:** `https://your-app.vercel.app/results`

---

## Support

If you encounter issues:
1. Check deployment logs
2. Review this troubleshooting section
3. Check GitHub issues
4. Review platform-specific documentation (Railway/Render/Vercel)
