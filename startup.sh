#!/bin/bash

echo "========================================="
echo "🎮 Teto Mario - Railway Deployment"
echo "========================================="

# 1. Обновляем список пакетов
echo "📦 Updating package list..."
apt-get update

# 2. Устанавливаем системные зависимости для Pygame
echo "📦 Installing system dependencies for Pygame..."
apt-get install -y \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libsdl2-dev \
    libsdl2-mixer-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    libx11-6 \
    libx11-dev \
    libxrandr2 \
    libxinerama1 \
    libxcursor1 \
    libxi6

echo "✅ System dependencies installed"

# 3. Проверяем наличие файлов
echo "📁 Checking project files..."
if [ -f "game.py" ]; then
    echo "✅ game.py found"
else
    echo "❌ game.py not found!"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "⚠️ requirements.txt not found, creating..."
    echo "pygame" > requirements.txt
fi

# 4. Устанавливаем Python зависимости
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# 5. Проверяем наличие ассетов
echo "📁 Checking assets..."
if [ -f "teto.png" ]; then
    echo "✅ teto.png found"
else
    echo "⚠️ teto.png not found (will use placeholder)"
fi

if [ -f "miku.png" ]; then
    echo "✅ miku.png found"
else
    echo "⚠️ miku.png not found (will use placeholder)"
fi

if [ -f "bg.jpg" ]; then
    echo "✅ bg.jpg found"
else
    echo "⚠️ bg.jpg not found (will use placeholder)"
fi

if [ -f "grass.jpg" ]; then
    echo "✅ grass.jpg found"
else
    echo "⚠️ grass.jpg not found (will use placeholder)"
fi

if [ -f "kurymdik.mp3" ]; then
    echo "✅ kurymdik.mp3 found"
else
    echo "⚠️ kurymdik.mp3 not found (sound disabled)"
fi

echo "========================================="
echo "🚀 Starting Teto Mario game..."
echo "🌐 Web server will run on port ${PORT:-8080}"
echo "========================================="

# 6. Запускаем игру
python game.py