# Manual Setup Guide - If Scripts Don't Work

## Windows - Manual Backend Setup

### Step 1: Open Command Prompt and navigate to backend
```cmd
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\backend
```

### Step 2: Create virtual environment
```cmd
python -m venv venv
```

### Step 3: Activate virtual environment
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` at the start of your command prompt line.

### Step 4: Upgrade pip
```cmd
python -m pip install --upgrade pip
```

### Step 5: Install dependencies
```cmd
pip install -r requirements.txt
```

### Step 6: Start the backend server
```cmd
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## Windows - Manual Frontend Setup

### Step 1: Open New Command Prompt and navigate to frontend
```cmd
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\frontend
```

### Step 2: Install dependencies
```cmd
npm install
```

This will take 2-5 minutes on first run.

### Step 3: Start the development server
```cmd
npm run dev
```

You should see:
```
▲ Next.js 16.0.3
- Local:        http://localhost:3000
```

---

## Mac/Linux - Manual Backend Setup

### Step 1: Open Terminal and navigate to backend
```bash
cd ~/Desktop/lagacyMap01/backend
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv
```

### Step 3: Activate virtual environment
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal.

### Step 4: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 5: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Start the backend server
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Mac/Linux - Manual Frontend Setup

### Step 1: Open New Terminal and navigate to frontend
```bash
cd ~/Desktop/lagacyMap01/frontend
```

### Step 2: Install dependencies
```bash
npm install
```

### Step 3: Start the development server
```bash
npm run dev
```

---

## Verification

### Check Backend is Running
Open browser and go to: `http://localhost:8000/docs`

You should see interactive API documentation.

### Check Frontend is Running
Open browser and go to: `http://localhost:3000`

You should see the LegacyMap landing page.

---

## Common Issues During Manual Setup

### "python: command not found"
**Solution:** Use `python3` instead
```bash
python3 -m venv venv
python3 -m pip install --upgrade pip
```

### "pip: command not found"
**Solution:** Use the full path
```bash
python -m pip install -r requirements.txt
```

### "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### "Port already in use"
**Backend:**
```cmd
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Update `frontend/.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8001
```

**Frontend:**
```cmd
npm run dev -- -p 3001
```

### "Module not found" errors
**Backend:**
```bash
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
rm -rf node_modules
npm install
```

### Virtual environment won't activate
Try using the Python directly:
```cmd
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Final Check

Once both services are running:

1. ✅ Backend running on `http://localhost:8000`
2. ✅ Frontend running on `http://localhost:3000`
3. ✅ Open `http://localhost:3000` in browser
4. ✅ Click "Get Started"
5. ✅ Create a test ZIP file with some code
6. ✅ Upload and test the analysis

---

## Keeping Services Running

### Important: Don't close the terminals!

- **Terminal 1:** Backend (keep running)
- **Terminal 2:** Frontend (keep running)
- **Terminal 3:** Browser (to test)

If you close either terminal, the service stops.

To stop a service:
- Press `Ctrl+C` in the terminal running it

---

## Help & Support

If something still doesn't work:
1. Check the terminal output for error messages
2. Copy error message and Google it
3. Check `TROUBLESHOOTING.md`
4. Verify Python version: `python --version` (should be 3.8+)
5. Verify Node version: `node --version` (should be 16+)

---

## Quick Reference

### Backend Commands
```bash
cd backend
python -m venv venv           # Create venv
venv\Scripts\activate.bat     # Activate (Windows)
source venv/bin/activate      # Activate (Mac/Linux)
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Commands
```bash
cd frontend
npm install
npm run dev
```

### Check if Running
- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`
