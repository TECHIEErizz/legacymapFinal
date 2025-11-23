# Troubleshooting Guide - LegacyMap

## Common Issues & Solutions

### Backend Issues

#### 1. **"ModuleNotFoundError" when starting backend**

**Problem:** Python modules not installed

**Solution:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat  # Windows
# or: source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

#### 2. **Port 8000 already in use**

**Problem:** Another application is using port 8000

**Solutions:**
```bash
# Option 1: Use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Option 2: Kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 3: Kill process using port 8000 (Mac/Linux)
lsof -i :8000
kill -9 <PID>
```

#### 3. **"No module named 'fastapi'"**

**Problem:** Dependencies not installed

**Solution:**
```bash
# Install all requirements
pip install -r requirements.txt

# Or install individually
pip install fastapi==0.95.2
pip install uvicorn==0.22.0
pip install aiofiles==23.1.0
pip install python-multipart==0.0.6
pip install networkx==3.1
```

#### 4. **CORS errors in frontend console**

**Problem:** Frontend can't communicate with backend

**Solutions:**
1. **Verify backend is running:**
   ```bash
   # Should see Uvicorn server running
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Check CORS configuration in `backend/app/main.py`:**
   - Should have your frontend URL in `allow_origins`
   - Default: `["http://localhost:3000", "http://localhost:3001"]`

3. **Verify frontend .env.local:**
   ```
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

4. **Clear browser cache:**
   - Press F12 → Settings → Storage → Clear Site Data

#### 5. **Temporary files not being cleaned up**

**Problem:** Old ZIP files accumulate in temp folder

**Solution:**
```bash
# Manual cleanup on Windows
rmdir /s /q %TEMP%\legacymap_*

# Manual cleanup on Mac/Linux
rm -rf /tmp/legacymap_*
```

---

### Frontend Issues

#### 1. **"npm not found"**

**Problem:** Node.js or npm not installed

**Solution:**
- Download and install Node.js from https://nodejs.org/
- Restart terminal/command prompt

#### 2. **Module resolution errors**

**Problem:** Dependencies not installed

**Solutions:**
```bash
cd frontend

# Clear node_modules
rm -rf node_modules  # Mac/Linux
rmdir /s /q node_modules  # Windows

# Clear lock file
rm package-lock.json  # Mac/Linux
del package-lock.json  # Windows

# Reinstall
npm install
```

#### 3. **"Backend not responding" errors**

**Problem:** Frontend can't reach backend API

**Check list:**
1. ✅ Backend is running on `http://localhost:8000`
2. ✅ Frontend .env.local has correct URL
3. ✅ No firewall blocking port 8000
4. ✅ Frontend can access the URL in browser

**Solution:**
```bash
# Test backend directly in browser
http://localhost:8000/docs

# If that works, check frontend URL config
# Edit frontend/.env.local:
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Restart frontend
npm run dev
```

#### 4. **Port 3000 already in use**

**Problem:** Another application is using port 3000

**Solutions:**
```bash
# Option 1: Use a different port
npm run dev -- -p 3001

# Option 2: Kill process using port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Option 3: Kill process using port 3000 (Mac/Linux)
lsof -i :3000
kill -9 <PID>
```

#### 5. **Tailwind CSS not loading**

**Problem:** Styles not applied

**Solution:**
```bash
# Rebuild CSS
npm run build

# Or restart dev server
npm run dev
```

---

### Integration Issues

#### 1. **File upload fails**

**Problem:** Upload not working or file not processing

**Check:**
1. ✅ File is a valid ZIP
2. ✅ Backend is running
3. ✅ No firewall/antivirus blocking upload
4. ✅ File size is reasonable (< 100MB recommended)

**Solution:**
```bash
# Check backend logs for errors
# Look for error messages in backend terminal
# Verify ZIP file is valid:
unzip -t yourfile.zip
```

#### 2. **Analysis results not showing**

**Problem:** Upload succeeds but no results appear

**Debug:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Attempt upload
4. Check response for errors
5. Look at backend logs for errors

**Solution:**
- Check backend console for error messages
- Verify uploaded ZIP has code files
- Try with smaller ZIP file first

#### 3. **Slow or hanging analysis**

**Problem:** Analysis takes very long or gets stuck

**Solutions:**
```bash
# For large codebases:
# 1. Split into smaller projects
# 2. Exclude node_modules, .git, build folders

# Restart backend if stuck:
# Kill and restart backend service
```

---

### Setup Issues

#### 1. **Virtual environment not activating (Python)**

**Windows:**
```bash
# If venv\Scripts\activate.bat doesn't work, try:
venv\Scripts\activate

# If that doesn't work, run cmd as Administrator
```

**Mac/Linux:**
```bash
# If source venv/bin/activate doesn't work, try:
. venv/bin/activate

# Check Python version
python --version
```

#### 2. **Wrong Python version**

**Solution:**
```bash
# Check current Python
python --version

# If you have multiple versions:
python3 -m venv venv  # Use Python 3
python3 -m pip install -r requirements.txt
```

---

### Docker Issues

#### 1. **Docker build fails**

**Problem:** Docker image won't build

**Solutions:**
```bash
# Clear Docker cache
docker system prune -a

# Build again
docker-compose build --no-cache

# Check Docker installation
docker --version
```

#### 2. **Containers won't start**

**Problem:** docker-compose up fails

**Solutions:**
```bash
# Check logs
docker-compose logs

# Rebuild and restart
docker-compose down
docker-compose up --build
```

---

## Debugging Checklist

Before reporting issues, verify:

- [ ] Backend running at `http://localhost:8000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] Both in same network (or properly configured)
- [ ] Firewall not blocking ports 3000 and 8000
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables set correctly
- [ ] No conflicting applications on same ports
- [ ] Browser cache cleared
- [ ] Latest version of Node.js installed

## Getting More Help

1. **Check Backend Logs:**
   - Look at terminal where backend is running
   - Search for "ERROR" messages

2. **Check Frontend Console:**
   - Press F12 in browser
   - Go to Console tab
   - Look for red error messages

3. **Test Endpoints Manually:**
   ```bash
   # Test backend health
   curl http://localhost:8000/docs
   ```

4. **Check Documentation:**
   - `SETUP_GUIDE.md` - Detailed setup
   - `QUICK_START.md` - Quick reference
   - `backend/README.md` - Backend info
   - `frontend/README.md` - Frontend info

---

## Performance Tips

1. **For Large Codebases:**
   - Upload files smaller than 50MB
   - Exclude node_modules, .git, build folders
   - Consider splitting into multiple uploads

2. **For Faster Analysis:**
   - Use faster storage (SSD)
   - Close other applications
   - Increase RAM if available

3. **For Production:**
   - Use docker-compose for consistent setup
   - Configure environment variables properly
   - Use reverse proxy (nginx) for frontend
   - Use process manager (PM2) for backend
