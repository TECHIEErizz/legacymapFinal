# ⚡ QUICK FIX - Direct Commands for Windows

## The Issue
Frontend showed "localhost refused to connect" - backend wasn't running.

## The Solution

### Terminal 1: Start Backend Directly

```powershell
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\backend
python -m pip install -r requirements.txt --quiet
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend Directly

```powershell
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\frontend
npm install
npm run dev
```

**Wait for this message:**
```
  ▲ Next.js 16.0.3
  - Local:        http://localhost:3000
```

### Terminal 3: Open Browser

```
http://localhost:3000
```

---

## Step-by-Step

1. **Open Command Prompt/PowerShell #1**
   - Copy & paste backend command above
   - Wait for "Application startup complete"
   - DON'T close this terminal!

2. **Open Command Prompt/PowerShell #2**
   - Copy & paste frontend command above
   - Wait for "Next.js 16.0.3"
   - DON'T close this terminal!

3. **Open Browser**
   - Type: `http://localhost:3000`
   - You should see LegacyMap landing page

---

## Troubleshooting This

### Backend won't start - "ModuleNotFoundError"
```powershell
python -m pip install fastapi uvicorn aiofiles python-multipart networkx
```

### Frontend won't start - "npm: command not found"
- Install Node.js from https://nodejs.org/
- Restart PowerShell/CMD
- Try `npm install` again

### "Port already in use" error
```powershell
# Use different port
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Then update frontend .env.local:
NEXT_PUBLIC_BACKEND_URL=http://localhost:8001
```

---

## ✅ Verify It's Working

### Backend Check
Open browser: `http://localhost:8000/docs`
- Should show Swagger API documentation

### Frontend Check
Open browser: `http://localhost:3000`
- Should show LegacyMap landing page

### Both Working
- Click "Get Started" on landing page
- Upload a test ZIP file
- See analysis results

---

## Keep These Running

⚠️ **IMPORTANT**: Both terminals must stay open!
- Terminal 1: Backend (running Python)
- Terminal 2: Frontend (running npm)
- Terminal 3: Browser (for testing)

If you close either terminal, that service stops.

---

**Copy the commands above and run them now!** 🚀
