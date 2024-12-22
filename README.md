# Whatsapp-Stalker

*I am not the creep that requested this tool; I just made it! 😉*

This script monitors the online status of a specific contact on WhatsApp Web and logs any changes (e.g., online, typing, offline) with timestamps into a CSV file. It's designed purely for educational purposes or legitimate use cases, so use it responsibly.

---

## Features
- **Real-time Monitoring**: Detects changes in the online status of a specified contact.
- **Logging**: Records all status changes with timestamps into a CSV file.
- **Simple Setup**: Easy-to-use script with minimal configuration.

---

## How to Use

1. **Clone or download this repository** to your local machine.
2. **Install Required Software**:
   - Download [Google Chrome](https://www.google.com/chrome/).
   - Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version.
   - Place the ChromeDriver executable in a known location (e.g., `C:\path\to\chromedriver.exe`).
3. **Install Required Python Libraries**:
   Run the following command in your terminal or command prompt:
   ```bash
   pip install selenium pandas
   ```
4. **Configure the Script**:
   - Open the script in a text editor.
   - Update the `CHROMEDRIVER_PATH` variable with the path to your ChromeDriver executable.
   - Replace the `CONTACT_NAME` variable with the exact name of the contact you want to monitor.
5. **Run the Script**:
   - Launch the script:
     ```bash
     python main.py
     ```
   - Open WhatsApp Web in Chrome and scan the QR code to log in.
   - Once logged in, press Enter in the terminal to start monitoring.
6. **Stop Monitoring**:
   - Press `Ctrl + C` in the terminal to stop the script.

---

## Output
The script creates a CSV file (`status_log.csv`) in the same directory, containing two columns:
- **Timestamp**: The date and time of the status change.
- **Status**: The updated status (e.g., online, typing, offline).

---

## Important Notes
- **Privacy**: Use this script responsibly. Monitoring someone's activity without consent may violate privacy laws.
- **Educational Purpose Only**: This tool is intended for learning how to use Selenium and Python automation, not for unethical use.
- **Limitations**:
  - The script relies on the structure of WhatsApp Web and may stop working if WhatsApp updates its UI.
  - The contact must already be visible in your chat list.

---

## License
This project is shared under the MIT License. Please see the `LICENSE` file for details.

---

## Disclaimer
I did not request this tool and am not responsible for how it’s used. If you have ethical concerns about using it, *don't use it*.
