# Deployment Instructions

## Deploy on Render (Free)

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login with GitHub**
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub account**
5. **Select `Elden-Ring-Dataset-API` repository**
6. **Configure:**
   - **Name**: `eldenring-api`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
7. **Environment Variables:**
   - `DATA_DIR` = `/opt/render/project/src/data`
   - `SECRET_KEY` = `EldenRing-API-Secret-Key-2024`

8. **Click "Create Web Service"**

## Alternative Free Platforms

### Railway.app
1. Go to [railway.app](https://railway.app)
2. "Deploy from GitHub"
3. Select your repo
4. Set environment variables

### Fly.io
```bash
fly auth login
fly launch
```

### PythonAnywhere
1. Upload your code
2. Configure WSGI
3. Set environment variables

## After Deployment

Your API will be available at:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.railway.app`
- Fly.io: `https://your-app-name.fly.dev`

Test endpoints:
- Root: `GET /`
- Docs: `GET /docs`
- Token: `POST /token`