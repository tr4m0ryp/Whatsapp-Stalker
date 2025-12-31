#!/bin/bash

# Quick Installer for WhatsApp Stalker on macOS High Sierra
# This script installs Chromium, ChromeDriver, and Python dependencies

echo "=========================================="
echo "WhatsApp Stalker - macOS High Sierra"
echo "Quick Installer"
echo "=========================================="
echo ""

# Create temp directory
TEMP_DIR="$HOME/whatsapp_stalker_temp"
mkdir -p "$TEMP_DIR"

# Check Python version
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found! Please install Python first."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✓ Found $PYTHON_VERSION"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
$PIP_CMD install --user pandas selenium || $PIP_CMD install pandas selenium

# Download and install Chromium
if [ ! -d "/Applications/Chromium.app" ]; then
    echo ""
    echo "Downloading Chromium for macOS..."
    echo "This may take a few minutes..."

    cd "$TEMP_DIR"
    curl -L -o chromium.zip "https://download-chromium.appspot.com/dl/Mac?type=snapshots"

    echo "Extracting Chromium..."
    unzip -q chromium.zip

    echo " Installing Chromium to /Applications..."
    if [ -d "chrome-mac/Chromium.app" ]; then
        sudo mv chrome-mac/Chromium.app /Applications/
    elif [ -d "Chromium.app" ]; then
        sudo mv Chromium.app /Applications/
    fi

    echo "Removing quarantine attribute..."
    sudo xattr -rd com.apple.quarantine /Applications/Chromium.app

    rm chromium.zip
    rm -rf chrome-mac
else
    echo "✓ Chromium is already installed"
fi

# Download and install ChromeDriver
if ! command -v chromedriver &> /dev/null && [ ! -f "/usr/local/bin/chromedriver" ]; then
    echo ""
    echo "Downloading ChromeDriver..."

    cd "$TEMP_DIR"
    # Get compatible ChromeDriver version for High Sierra (version 103 - last version for macOS 10.13)
    curl -L -o chromedriver.zip "https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_mac64.zip"

    echo "📦 Extracting ChromeDriver..."
    unzip -q chromedriver.zip

    echo "📂 Installing ChromeDriver..."
    chmod +x chromedriver
    sudo mv chromedriver /usr/local/bin/

    echo "🔓 Removing quarantine attribute..."
    sudo xattr -d com.apple.quarantine /usr/local/bin/chromedriver 2>/dev/null || true

    rm chromedriver.zip
else
    echo "✓ ChromeDriver is already installed"
    # Try to remove quarantine just in case
    sudo xattr -d com.apple.quarantine /usr/local/bin/chromedriver 2>/dev/null || true
fi

# Clean up temp directory
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "📱 Starting WhatsApp Stalker..."
echo ""
echo "Instructions:"
echo "1. Chromium browser will open"
echo "2. Scan the QR code with WhatsApp on your phone"
echo "3. Press Enter in this terminal once logged in"
echo "4. The bot will monitor the contact status"
echo ""
echo "Press Ctrl+C to stop monitoring"
echo ""
sleep 3

# Run the main.py script
$PYTHON_CMD main.py
