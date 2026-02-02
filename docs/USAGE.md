# Usage Guide

## Setting Up WhatsApp Monitor

### 1. Prerequisites

- Python 3.8 or higher
- Google Chrome or Chromium browser
- ChromeDriver matching your browser version

### 2. Installation

```bash
# Clone repository
git clone https://github.com/tr4m0ryp/Whatsapp-Stalker.git
cd Whatsapp-Stalker

# Install Python dependencies
pip install -r requirements.txt

# Configure
cp config/config.example.py config/config.py
nano config/config.py  # Edit with your settings
```

### 3. Configuration Options

Edit `config/config.py`:

```python
# Required: Contact name exactly as shown in WhatsApp
CONTACT_NAME = "John Doe"

# Optional: Check interval (seconds)
CHECK_INTERVAL = 5

# Optional: Log directory
LOGS_DIR = "logs"
```

### 4. Running the Monitor

```bash
python src/monitor.py
```

Follow prompts:
1. QR code will appear in browser - scan with phone
2. Press Enter in terminal when logged in
3. Monitor will begin tracking

### 5. Output

Logs are saved to `logs/status_log_YYYYMMDD_HHMMSS.csv`:

```csv
Timestamp,Status
2024-12-22 14:30:00,offline
2024-12-22 14:35:22,online
2024-12-22 14:36:10,offline
```

### 6. Debugging

If status detection fails:

```bash
python scripts/debug.py
```

This opens WhatsApp Web and analyzes the DOM structure to help troubleshoot.

### 7. Troubleshooting

**ChromeDriver not found:**
```bash
# macOS
brew install chromedriver

# Ubuntu/Debian
sudo apt install chromium-chromedriver

# Verify installation
chromedriver --version
```

**Contact not found:**
- Ensure contact name matches exactly (case-sensitive)
- Contact must be visible in chat list
- Try using debug script to verify XPath selectors

**Status not detected:**
- WhatsApp Web UI may have changed
- Use debug script to inspect current DOM structure
- Update XPaths in `src/monitor.py` if needed

---

## Privacy & Legal Considerations

- Always obtain consent before monitoring
- Respect WhatsApp Terms of Service
- Check local laws regarding monitoring
- Use only for legitimate purposes

Repository made by openclaw
