# LegacyMap - Full Stack Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or pnpm
- Git

## Backend Setup (Python)

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create Python virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment
**Windows:**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the backend server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start at `http://localhost:8000`

## Frontend Setup (Next.js)

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
# or
pnpm install
```

### 3. Configure environment
Check `.env.local` file - it should have:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 4. Run the frontend server
```bash
npm run dev
# or
pnpm dev
```

The frontend will start at `http://localhost:3000`

## Running Both Services

### Option 1: Terminal Windows
1. Open Terminal 1 for backend:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate.bat  # Windows or source venv/bin/activate for Mac/Linux
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Open Terminal 2 for frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Option 2: Quick Start Scripts
**Windows:**
- Backend: Double-click `backend/start.bat`
- Frontend: Run `cd frontend && npm install && npm run dev`

**macOS/Linux:**
```bash
# Terminal 1
cd backend && bash start.sh

# Terminal 2
cd frontend && bash start.sh
```

## API Endpoints

### `/upload` (POST)
- Accepts ZIP file upload
- Returns dependency analysis
- Response includes:
  - `summary`: Total files, LOC, top risky files
  - `nodes`: File metadata with dependencies
  - `edges`: Dependency relationships
  - `components`: Circular dependencies

### `/upload-analyze` (POST)
- Upload and get detailed analysis
- Includes function/class extraction
- Response format compatible with frontend

### `/function-details/{repo_id}/{file_path}/{function_name}` (GET)
- Get where a function is called
- Get function dependencies
- Returns call sites and dependencies tables

## Testing the Integration

1. Start both backend and frontend
2. Open `http://localhost:3000` in browser
3. Click "Get Started"
4. Create a ZIP file with your code
5. Upload the ZIP file
6. View the analysis results

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Change port in startup command
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
# Update frontend .env.local to match
```

**Python module not found:**
```bash
pip install -r requirements.txt
```

**CORS errors:**
- Check that frontend URL is in `app.main.CORS allow_origins`
- Default: localhost:3000, localhost:3001

### Frontend Issues

**Module not found errors:**
```bash
rm -rf node_modules pnpm-lock.yaml
npm install
```

**Backend not responding:**
- Verify backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_BACKEND_URL`
- Check browser console for errors

## Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── scanner.py       # Code analysis
│   │   ├── function_extractor.py  # Function/class extraction
│   │   ├── utils.py         # Utilities
│   │   └── __init__.py
│   ├── requirements.txt      # Python dependencies
│   └── start.bat            # Windows startup script
│
└── frontend/
    ├── app/
    │   ├── page.tsx         # Main page
    │   ├── layout.tsx       # Layout
    │   └── globals.css      # Global styles
    ├── components/          # React components
    ├── public/              # Static files
    ├── package.json         # npm dependencies
    └── .env.local           # Environment variables
```

## Key Features

1. **Code Analysis**
   - Scans JavaScript, TypeScript, and Python files
   - Extracts functions and classes
   - Builds dependency graphs
   - Calculates risk scores

2. **Visualization**
   - Dashboard with metrics
   - Function list with search
   - Dependency visualization
   - Risk assessment

3. **Performance**
   - Fast ZIP file processing
   - Async operations
   - Real-time updates

## Environment Variables

### Backend
- `UVICORN_HOST`: Server host (default: 0.0.0.0)
- `UVICORN_PORT`: Server port (default: 8000)

### Frontend
- `NEXT_PUBLIC_BACKEND_URL`: Backend API URL (default: http://localhost:8000)

## Production Deployment

### Backend (Docker)
```bash
cd backend
docker build -t legacymap-backend .
docker run -p 8000:8000 legacymap-backend
```

### Frontend (Docker)
```bash
cd frontend
docker build -t legacymap-frontend .
docker run -p 3000:3000 legacymap-frontend
```

## Support & Documentation

For more information, check:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Architecture: `backend/ARCHITECTURE.md`
