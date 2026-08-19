#!/bin/bash

echo "========================================="
echo "🎮 Teto Mario - Railway Deployment"
echo "========================================="

# Устанавливаем зависимости
apt-get update
apt-get install -y \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libsdl2-dev

# Проверяем файлы
echo "📁 Checking project files..."
if [ -f "game.py" ]; then
    echo "✅ game.py found"
else
    echo "❌ game.py not found!"
    exit 1
fi

# Устанавливаем Python зависимости
pip install --no-cache-dir -r requirements.txt

echo "========================================="
echo "🚀 Starting Teto Mario game..."
echo "========================================="

# Запускаем игру
python game.py
