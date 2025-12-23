#!/bin/bash

echo "========================================"
echo " Social Media Platform - Startup Script"
echo "========================================"
echo ""
echo "This will start all three services:"
echo "1. Backend API (Port 8000)"
echo "2. Frontend (Port 3000)"
echo "3. Sentiment Analysis API (Port 8001)"
echo ""
echo "Press Ctrl+C in any terminal to stop that service"
echo ""
read -p "Press enter to continue..."

echo "Starting Backend..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/social-media-platform/backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"' &

sleep 3

echo "Starting Frontend..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/social-media-platform/frontend && npm run dev"' &

sleep 3

echo "Starting Sentiment Analysis..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/sentiment-analysis-engine && source venv/bin/activate && uvicorn app.main:app --reload --port 8001"' &

echo ""
echo "========================================"
echo "All services are starting!"
echo "========================================"
echo ""
echo "URLs:"
echo "Frontend:     http://localhost:3000"
echo "Backend API:  http://localhost:8000/docs"
echo "Sentiment:    http://localhost:8001/docs"
echo ""
echo "Three new terminal windows should have opened."
echo "Check each window for any errors."
echo ""
