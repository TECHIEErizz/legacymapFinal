# Quick Start - LegacyMap Full Stack

## ⚡ Windows Quick Start (Fastest)

### Option 1: Use Start Scripts (Recommended)

**Open Command Prompt 1 - Backend:**
```cmd
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\backend
start.bat
```

**Open Command Prompt 2 - Frontend:**
```cmd
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\frontend
start.bat
```

Wait for messages showing:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Option 2: Manual Setup (If scripts fail)
See `MANUAL_SETUP.md` for step-by-step instructions.

### Step 2: Access the Application
Open browser: **`http://localhost:3000`**

---

## 🐧 macOS/Linux Quick Start

### Terminal 1 - Backend:
```bash
cd ~/Desktop/lagacyMap01/backend
bash start.sh
```

### Terminal 2 - Frontend:
```bash
cd ~/Desktop/lagacyMap01/frontend
bash start.sh
```

### Open Browser
Go to: **`http://localhost:3000`**

---

## 🎯 What You'll See

1. **Landing Page** - Welcome screen with features
2. **Click "Get Started"**
3. **Upload Page** - Drag & drop your code ZIP file
4. **Dashboard** - View analysis results:
   - Total files analyzed
   - Total lines of code
   - Functions/classes found
   - Risk scoring
   - Dependency graph

---

## 🆘 Quick Troubleshooting

### Backend won't start?
See **`MANUAL_SETUP.md`** → Backend setup section

### Frontend won't start?
See **`MANUAL_SETUP.md`** → Frontend setup section

### CORS errors?
1. Make sure backend is running: `http://localhost:8000/docs`
2. Check frontend .env.local has: `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`
3. Restart both services

### Port already in use?
See **`TROUBLESHOOTING.md`** → "Port already in use"

---

## 📚 Full Documentation

- `MANUAL_SETUP.md` - Manual step-by-step guide
- `SETUP_GUIDE.md` - Detailed setup
- `TROUBLESHOOTING.md` - Common issues
- `API_DOCUMENTATION.md` - API reference

---

## ✅ Verify Setup

Backend is working if you see at: `http://localhost:8000/docs`
- Swagger UI with API endpoints

Frontend is working if you see at: `http://localhost:3000`
- LegacyMap landing page with features

Both working? Upload a ZIP file and test! 🚀
