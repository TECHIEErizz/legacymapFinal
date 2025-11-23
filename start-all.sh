#!/bin/bash

echo "🚀 Starting LegacyMap Full Stack..."

# Start Backend
echo "Starting Backend..."
cd backend
bash start.sh &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
bash start.sh &
FRONTEND_PID=$!
cd ..

echo "✅ Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Application will be available at http://localhost:3000"
echo "Press Ctrl+C to stop both services"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

wait
