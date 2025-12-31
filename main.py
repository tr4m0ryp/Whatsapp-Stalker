import time
import pandas as pd
import shutil
import os
import platform
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Try to automatically locate chromedriver in PATH. If not found, fall back to
# a sensible default for the current platform and instruct the user to install
# or set the correct path.
CHROMEDRIVER_PATH = shutil.which("chromedriver")
if CHROMEDRIVER_PATH:
    print(f"Found chromedriver at: {CHROMEDRIVER_PATH}")
else:
    if platform.system() == "Windows":
        # Keep the original placeholder for Windows users. They should update it
        # to the actual chromedriver.exe path (raw string format is fine).
        CHROMEDRIVER_PATH = r"C:\\path\\to\\chromedriver.exe"
    else:
        # Common Linux location; many package managers place chromedriver here.
        CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

    if not os.path.exists(CHROMEDRIVER_PATH):
        print("\nchromedriver not found on this system.\n"
              f"Tried: {CHROMEDRIVER_PATH} and PATH search.\n"
              "Please install ChromeDriver for your Chrome/Chromium version and either:"
              "\n  - put the chromedriver executable in your PATH (so `chromedriver` is found),"
              "\n  - or set CHROMEDRIVER_PATH in this script to the full path of chromedriver.\n")
        sys.exit(1)
CONTACT_NAME = "M met lange naam" #here the person you would love to stalk
CHECK_INTERVAL = 5

# Create logs directory if it doesn't exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Create timestamped log file to preserve old logs
log_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
csv_file = os.path.join(logs_dir, f'status_log_{log_timestamp}.csv')

# Initialize CSV file with headers
df = pd.DataFrame(columns=["Timestamp", "Status"])
df.to_csv(csv_file, index=False)

def get_contact_status(driver, contact_name):
    try:
        # Check if the chat is already open to avoid unnecessary clicks
        is_chat_open = False
        try:
            # Look for the contact name in the header
            # The header usually contains a span with the contact name as title
            header_title = driver.find_element(By.XPATH, f'//header//span[@title="{contact_name}"]')
            if header_title.is_displayed():
                is_chat_open = True
        except NoSuchElementException:
            pass

        if not is_chat_open:
            chat_xpath = f'//span[@title="{contact_name}"]'
            chat = driver.find_element(By.XPATH, chat_xpath)
            chat.click()
            # Wait briefly for the chat header to load
            time.sleep(1.5)

        # Try to find status using the XPath that works (from debug output)
        status_text = ""

        # Method 1: Check for specific status texts (searches all possible status indicators)
        status_xpaths = [
            '//header//span[contains(text(), "online")]',
            '//header//span[contains(text(), "typing")]',
            '//header//span[contains(text(), "recording")]',  # Voice message
            '//header//span[contains(text(), "last seen")]',
            '//header//span[contains(text(), "click here")]',  # No status visible
        ]

        for xpath in status_xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    status_text = elements[0].text.strip().lower()
                    break
            except:
                continue

        # Method 2: If nothing found, check the following-sibling elements (backup method)
        if not status_text:
            try:
                elements = driver.find_elements(By.XPATH, '//header//div[@role="button"]//following-sibling::*')
                for elem in elements:
                    text = elem.text.strip().lower()
                    # Check if this element contains any status-related text
                    if any(keyword in text for keyword in ["online", "typing", "recording", "last seen", "click here"]):
                        status_text = text
                        break
            except:
                pass

        # Determine the final status based on what we found
        if "online" in status_text:
            return "online"
        elif "typing" in status_text:
            return "typing..."
        elif "recording" in status_text:
            return "recording..."
        elif "last seen" in status_text:
            return "offline"
        elif "click here" in status_text:
            return "offline (no status)"
        elif not status_text:
            # No status text found at all (privacy settings or not loaded)
            return "offline (no status)"
        else:
            # Unknown status text - log it for debugging
            return f"offline ({status_text[:20]})"

    except (NoSuchElementException, TimeoutException):
        return "offline (error)"

service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()

# Try to find Chromium binary
chromium_paths = [
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
]

for chromium_path in chromium_paths:
    if os.path.exists(chromium_path):
        options.binary_location = chromium_path
        print(f"Using browser at: {chromium_path}")
        break

options.add_argument("--start-maximized")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://web.whatsapp.com/')
print("Scan the QR code to log in to WhatsApp Web.")
input("Press Enter once you are logged in...")

prev_status = None

try:
    while True:
        current_status = get_contact_status(driver, CONTACT_NAME)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if current_status != prev_status:
            print(f"{timestamp} - {CONTACT_NAME} is now {current_status}.")
            df_new = pd.DataFrame([[timestamp, current_status]], columns=["Timestamp", "Status"])
            df_new.to_csv(csv_file, mode='a', header=False, index=False)
            prev_status = current_status

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")
finally:
    driver.quit()
