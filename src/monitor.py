"""
WhatsApp Online Status Monitor

Monitors WhatsApp Web for contact status changes and logs to CSV.

Author: tr4m0ryp
Date: 2024-12-22
Repository: https://github.com/tr4m0ryp/Whatsapp-Stalker
"""

import time
import os
import sys
import shutil
import platform
from datetime import datetime
from typing import Optional

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_chromedriver_path() -> str:
    """
    Locate ChromeDriver executable.
    
    Returns:
        Path to chromedriver executable
        
    Raises:
        SystemExit: If chromedriver not found
    """
    chromedriver_path = shutil.which("chromedriver")
    
    if chromedriver_path:
        print(f"Found chromedriver at: {chromedriver_path}")
        return chromedriver_path
    
    # Platform-specific defaults
    if platform.system() == "Windows":
        chromedriver_path = r"C:\path\to\chromedriver.exe"
    else:
        chromedriver_path = "/usr/bin/chromedriver"
    
    if not os.path.exists(chromedriver_path):
        print("\nERROR: chromedriver not found on this system.")
        print(f"Tried: {chromedriver_path} and PATH search.")
        print("\nPlease install ChromeDriver:")
        print("  - macOS: brew install chromedriver")
        print("  - Linux: sudo apt install chromium-chromedriver")
        print("  - Or download from: https://chromedriver.chromium.org/")
        sys.exit(1)
    
    return chromedriver_path


def load_config() -> dict:
    """
    Load configuration from config module.
    
    Returns:
        Dictionary with configuration settings
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
    sys.path.insert(0, config_path)
    
    try:
        import config
        return {
            'CONTACT_NAME': getattr(config, 'CONTACT_NAME', 'Contact Name'),
            'CHECK_INTERVAL': getattr(config, 'CHECK_INTERVAL', 5),
            'LOGS_DIR': getattr(config, 'LOGS_DIR', 'logs')
        }
    except ImportError:
        print("WARNING: config.py not found. Using defaults.")
        print("Copy config/config.example.py to config/config.py and customize.")
        return {
            'CONTACT_NAME': 'Contact Name',
            'CHECK_INTERVAL': 5,
            'LOGS_DIR': 'logs'
        }


def setup_chrome_driver(chromedriver_path: str) -> webdriver.Chrome:
    """
    Initialize Chrome WebDriver with appropriate options.
    
    Args:
        chromedriver_path: Path to chromedriver executable
        
    Returns:
        Configured Chrome WebDriver instance
    """
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    
    # Find Chrome/Chromium binary
    chromium_paths = [
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser"
    ]
    
    for chromium_path in chromium_paths:
        if os.path.exists(chromium_path):
            options.binary_location = chromium_path
            print(f"Using browser at: {chromium_path}")
            break
    
    # Browser options
    options.add_argument("--start-maximized")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(service=service, options=options)


def get_contact_status(driver: webdriver.Chrome, contact_name: str) -> str:
    """
    Retrieve current online status of specified contact.
    
    Args:
        driver: Selenium WebDriver instance
        contact_name: Name of contact to monitor
        
    Returns:
        Current status string (online, typing, offline, etc.)
    """
    try:
        # Check if chat is already open
        is_chat_open = False
        try:
            header_title = driver.find_element(
                By.XPATH, 
                f'//header//span[@title="{contact_name}"]'
            )
            if header_title.is_displayed():
                is_chat_open = True
        except NoSuchElementException:
            pass
        
        # Open chat if not already open
        if not is_chat_open:
            chat_xpath = f'//span[@title="{contact_name}"]'
            chat = driver.find_element(By.XPATH, chat_xpath)
            chat.click()
            time.sleep(1.5)  # Wait for chat to load
        
        # Check for status indicators
        status_xpaths = [
            ('//header//span[contains(text(), "online")]', 'online'),
            ('//header//span[contains(text(), "typing")]', 'typing'),
            ('//header//span[contains(text(), "recording")]', 'recording'),
            ('//header//span[contains(text(), "last seen")]', 'offline'),
        ]
        
        for xpath, status in status_xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    return status
            except Exception:
                continue
        
        return "offline"
        
    except (NoSuchElementException, TimeoutException) as e:
        return f"error: {str(e)}"


def initialize_log_file(logs_dir: str) -> str:
    """
    Create log directory and initialize CSV file.
    
    Args:
        logs_dir: Directory for log files
        
    Returns:
        Path to created CSV file
    """
    os.makedirs(logs_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(logs_dir, f'status_log_{timestamp}.csv')
    
    # Initialize with headers
    df = pd.DataFrame(columns=["Timestamp", "Status"])
    df.to_csv(csv_file, index=False)
    
    return csv_file


def log_status_change(csv_file: str, timestamp: str, status: str) -> None:
    """
    Append status change to CSV log.
    
    Args:
        csv_file: Path to CSV file
        timestamp: Timestamp string
        status: Status string
    """
    df = pd.DataFrame([[timestamp, status]], columns=["Timestamp", "Status"])
    df.to_csv(csv_file, mode='a', header=False, index=False)


def main() -> None:
    """Main entry point for WhatsApp monitor."""
    print("=" * 60)
    print("WhatsApp Online Status Monitor")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    contact_name = config['CONTACT_NAME']
    check_interval = config['CHECK_INTERVAL']
    logs_dir = config['LOGS_DIR']
    
    print(f"\nConfiguration:")
    print(f"  Contact: {contact_name}")
    print(f"  Check interval: {check_interval}s")
    print(f"  Logs directory: {logs_dir}")
    
    # Get ChromeDriver path
    chromedriver_path = get_chromedriver_path()
    
    # Initialize driver
    print("\nInitializing Chrome...")
    driver = setup_chrome_driver(chromedriver_path)
    
    # Open WhatsApp Web
    print("\nOpening WhatsApp Web...")
    driver.get('https://web.whatsapp.com/')
    print("Please scan the QR code to log in.")
    input("\nPress Enter once you are logged in...")
    
    # Initialize logging
    csv_file = initialize_log_file(logs_dir)
    print(f"\nLogging to: {csv_file}")
    
    # Start monitoring
    print(f"\nStarting monitoring for: {contact_name}")
    print("Press Ctrl+C to stop\n")
    
    prev_status = None
    
    try:
        while True:
            current_status = get_contact_status(driver, contact_name)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if current_status != prev_status:
                print(f"{timestamp} - {contact_name}: {current_status}")
                log_status_change(csv_file, timestamp, current_status)
                prev_status = current_status
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    finally:
        driver.quit()
        print(f"\nLog saved to: {csv_file}")


if __name__ == "__main__":
    main()
