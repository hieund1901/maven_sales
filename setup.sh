#!/bin/bash

# Tạo môi trường ảo (nếu chưa có)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.10 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt các phụ thuộc từ requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found."
fi

echo "Setup complete!"
