#!/bin/bash
set -e

# Build Angular frontend
echo "Building frontend..."
cd frontend
npm install
npm run build

# Install Python backend dependencies
echo "Installing backend dependencies..."
cd ../backend
pip install -r requirements.txt
