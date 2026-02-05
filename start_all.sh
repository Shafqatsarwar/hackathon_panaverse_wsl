#!/bin/bash

# Define project root
PROJECT_DIR="/home/shafqatsarwar/Projects/hackathon_panaverse_wsl"

echo "📂 Navigating to $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "❌ Failed to cd to $PROJECT_DIR"; exit 1; }

# 1. Kill invalid processes
echo "🧹 Cleaning up ports..."
fuser -k 8000/tcp > /dev/null 2>&1
fuser -k 3000/tcp > /dev/null 2>&1

# 2. Remove locks
echo "🔓 Removing lock files..."
rm -rf frontend/.next/dev/lock

# 3. Start Backend
echo "🚀 Starting Backend (port 8000)..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ .venv not found!"
    exit 1
fi

# Run in background, log to backend.log
nohup python3 src/api/chat_api.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# 4. Wait a moment for backend to initialize
echo "⏳ Waiting for backend to initialize..."
sleep 5

# 5. Start Frontend
echo "🎨 Starting Frontend (port 3000)..."
cd frontend || { echo "❌ frontend dir not found"; exit 1; }
# Run in background, log to frontend.log
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo "✅ All services started!"
echo "   Backend logs: tail -f $PROJECT_DIR/backend.log"
echo "   Frontend logs: tail -f $PROJECT_DIR/frontend.log"
echo "   App URL: http://localhost:3000"
