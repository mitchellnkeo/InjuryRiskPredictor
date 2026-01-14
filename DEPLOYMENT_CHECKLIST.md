# Deployment Checklist

Use this checklist to ensure everything is ready for deployment.

## Pre-Deployment

### Backend
- [x] Model files exist (`backend/models/random_forest_model.pkl`, `backend/models/scaler.pkl`)
- [x] Dockerfile created and tested
- [x] `.dockerignore` configured
- [x] CORS settings updated for production
- [x] Environment variable handling (PORT) configured
- [x] Health check endpoint working (`/health`)
- [x] API documentation accessible (`/docs`)

### Frontend
- [x] Next.js build succeeds (`npm run build`)
- [x] No TypeScript errors
- [x] Environment variables configured (`NEXT_PUBLIC_API_URL`)
- [x] API client configured
- [x] All pages render correctly

### Documentation
- [x] Deployment guide created (`docs/DEPLOYMENT.md`)
- [x] Quick start guide created (`DEPLOYMENT_QUICKSTART.md`)
- [x] Platform-specific configs created (Railway, Render, Vercel)

---

## Backend Deployment Steps

### Railway
- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Create new project
- [ ] Configure:
  - Root Directory: `.` (project root)
  - Dockerfile Path: `backend/Dockerfile`
- [ ] Set environment variables (if needed)
- [ ] Deploy
- [ ] Test health endpoint: `curl https://your-api.up.railway.app/health`
- [ ] Test API docs: Visit `https://your-api.up.railway.app/docs`
- [ ] Copy API URL for frontend

### Render
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Create new web service
- [ ] Configure:
  - Root Directory: `.`
  - Dockerfile Path: `backend/Dockerfile`
  - Docker Context: `.`
- [ ] Set environment variables (if needed)
- [ ] Deploy
- [ ] Test health endpoint: `curl https://your-api.onrender.com/health`
- [ ] Test API docs: Visit `https://your-api.onrender.com/docs`
- [ ] Copy API URL for frontend

---

## Frontend Deployment Steps

### Vercel
- [ ] Create Vercel account
- [ ] Connect GitHub repository
- [ ] Import project
- [ ] Configure:
  - Root Directory: `frontend`
  - Framework: Next.js (auto-detected)
- [ ] Set environment variable:
  - `NEXT_PUBLIC_API_URL`: Your backend URL
- [ ] Deploy
- [ ] Test:
  - Visit frontend URL
  - Test prediction form
  - Check browser console for errors
  - Verify API calls work

---

## Post-Deployment

### Backend
- [ ] Health check returns 200 OK
- [ ] API docs accessible
- [ ] Prediction endpoint works
- [ ] CORS configured for frontend URL
- [ ] Logs show no errors

### Frontend
- [ ] Site loads without errors
- [ ] Prediction form submits successfully
- [ ] Results page displays correctly
- [ ] No console errors
- [ ] API calls succeed
- [ ] Mobile responsive

### Integration
- [ ] Frontend can communicate with backend
- [ ] CORS errors resolved
- [ ] End-to-end prediction flow works
- [ ] Error handling works correctly

---

## Testing Commands

### Test Docker Build Locally
```bash
cd backend
./test_docker.sh
```

### Test Backend Health
```bash
curl https://your-api-url/health
```

### Test Prediction Endpoint
```bash
curl -X POST https://your-api-url/api/predict \
  -H "Content-Type: application/json" \
  -d @backend/test_request.json
```

### Test Frontend Build
```bash
cd frontend
npm run build
npm run start
```

---

## Troubleshooting

If deployment fails:

1. **Check logs** - Railway/Render/Vercel provide detailed build logs
2. **Verify file paths** - Ensure Dockerfile paths are correct
3. **Check environment variables** - Ensure all required vars are set
4. **Test locally first** - Use Docker build script to test before deploying
5. **Review documentation** - See `docs/DEPLOYMENT.md` for detailed troubleshooting

---

## Notes

- Model files must be committed to repository (or use external storage)
- CORS must be updated after frontend deployment
- Environment variables must be set in deployment platform
- Test locally before deploying to catch issues early
