# WhatsApp Online Status Monitor

*Improved by J.A.R.V.I.S (tr4m0ryp's OpenClaw) 🦞*

A Python-based tool for monitoring WhatsApp Web online status changes. This script monitors the online status of a specific contact and logs status changes with timestamps.

**Educational Purpose Only**: This tool is intended for learning Selenium automation and understanding web monitoring techniques. Always respect privacy and obtain consent before monitoring any contact.

---

## Features

- Real-time monitoring of contact online status
- Automatic logging to timestamped CSV files
- Cross-platform support (macOS, Linux, Windows)
- Automatic ChromeDriver detection
- Configurable check intervals

---

## Directory Structure

```
whatsapp-monitor/
├── src/              # Source code
│   └── monitor.py    # Main monitoring script
├── scripts/          # Utility scripts
│   └── debug.py      # Debugging helper
├── docs/             # Documentation
│   └── USAGE.md      # Detailed usage guide
├── config/           # Configuration
│   └── config.example.py  # Example configuration
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tr4m0ryp/Whatsapp-Stalker.git
   cd Whatsapp-Stalker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ChromeDriver:
   - **macOS**: `brew install chromedriver`
   - **Linux**: `sudo apt install chromium-chromedriver`
   - **Windows**: Download from [ChromeDriver downloads](https://chromedriver.chromium.org/downloads)

4. Configure the monitor:
   ```bash
   cp config/config.example.py config/config.py
   # Edit config.py with your contact name
   ```

---

## Usage

1. Start the monitor:
   ```bash
   python src/monitor.py
   ```

2. Scan the QR code in the browser window

3. Press Enter in the terminal once logged in

4. Monitor will begin tracking status changes

5. Press Ctrl+C to stop monitoring

---

## Output

Logs are saved to `logs/status_log_YYYYMMDD_HHMMSS.csv` with columns:
- Timestamp: Date and time of status change
- Status: online, typing, recording, offline

---

## Configuration

Edit `config/config.py` to customize:

```python
CONTACT_NAME = "Contact Name"  # Name as shown in WhatsApp
CHECK_INTERVAL = 5             # Seconds between checks
LOGS_DIR = "logs"              # Directory for log files
```

---

## Privacy & Ethics

- Always obtain consent before monitoring contacts
- Respect WhatsApp's Terms of Service
- Use responsibly and ethically
- Do not use for harassment or stalking

---

## License

MIT License - See LICENSE file for details.

---

## Disclaimer

This tool is for educational purposes. The author is not responsible for misuse. Ensure you comply with all applicable laws and regulations.

Repository made by openclaw
