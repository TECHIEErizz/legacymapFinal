# 🚀 LegacyMap - All-In-One Startup Guide

## Issue Fixed ✅

The `start.bat` script had an issue with command recognition. This is now **COMPLETELY FIXED** with:

1. ✅ Improved `start.bat` with error checking
2. ✅ PowerShell version `start.ps1` for Windows
3. ✅ Improved frontend `start.bat`
4. ✅ Complete manual setup guide (`MANUAL_SETUP.md`)
5. ✅ Updated `QUICK_START.md` with all options

---

## 🎯 Choose Your Setup Method

### Method 1: Use Start Scripts (Easiest)

**Windows:**
```cmd
# Terminal 1:
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\backend
start.bat

# Terminal 2:
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\frontend
start.bat
```

**Mac/Linux:**
```bash
# Terminal 1:
cd ~/Desktop/lagacyMap01/backend && bash start.sh

# Terminal 2:
cd ~/Desktop/lagacyMap01/frontend && bash start.sh
```

---

### Method 2: Use PowerShell (Windows Only)

```powershell
# Terminal 1:
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\backend
.\start.ps1

# Terminal 2:
cd C:\Users\deepanshu\OneDrive\Desktop\lagacyMap01\frontend
start.bat
```

---

### Method 3: Manual Setup (Complete Control)

See **`MANUAL_SETUP.md`** for detailed step-by-step instructions.

---

## ✅ Verification

### Backend Running?
Open in browser: `http://localhost:8000/docs`

Should show Swagger API documentation.

### Frontend Running?
Open in browser: `http://localhost:3000`

Should show LegacyMap landing page.

### Both Running?
1. Go to `http://localhost:3000`
2. Click "Get Started"
3. Upload a test ZIP file
4. View analysis results

---

## 📁 What Each File Does

| File | Purpose |
|------|---------|
| `backend/start.bat` | Start backend on Windows |
| `backend/start.ps1` | Start backend on Windows (PowerShell) |
| `backend/start.sh` | Start backend on Mac/Linux |
| `frontend/start.bat` | Start frontend on Windows |
| `frontend/start.sh` | Start frontend on Mac/Linux |

---

## 🔧 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Script won't run | Try `MANUAL_SETUP.md` |
| Port in use | See `TROUBLESHOOTING.md` |
| Dependencies missing | Run manual setup |
| CORS errors | Check `.env.local` config |
| Backend won't start | See `MANUAL_SETUP.md` |
| Frontend won't start | See `MANUAL_SETUP.md` |

---

## 📚 Documentation

- **QUICK_START.md** - 2-minute quick reference
- **MANUAL_SETUP.md** - Step-by-step manual setup
- **SETUP_GUIDE.md** - Comprehensive setup guide
- **TROUBLESHOOTING.md** - Common issues & solutions
- **API_DOCUMENTATION.md** - API reference

---

## ✨ Summary

Everything is now **FIXED and READY**:

✅ Backend startup script (improved)
✅ Frontend startup script (improved)
✅ PowerShell version (for Windows)
✅ Manual setup guide (complete)
✅ Updated quick start (with all options)

**Pick a method above and start! 🚀**
