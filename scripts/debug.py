"""
WhatsApp Debug Helper

Debug script for inspecting WhatsApp Web DOM structure.
Useful for troubleshooting status detection issues.

Author: tr4m0ryp
"""

import time
import os
import sys
import shutil
import platform
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_chromedriver_path() -> str:
    """Locate ChromeDriver executable."""
    chromedriver_path = shutil.which("chromedriver")
    
    if chromedriver_path:
        return chromedriver_path
    
    if platform.system() == "Windows":
        return r"C:\path\to\chromedriver.exe"
    return "/usr/bin/chromedriver"


def setup_driver(chromedriver_path: str) -> webdriver.Chrome:
    """Initialize Chrome WebDriver."""
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=service, options=options)


def inspect_header(driver: webdriver.Chrome, contact_name: str) -> None:
    """
    Inspect WhatsApp header structure for debugging.
    
    Args:
        driver: Selenium WebDriver instance
        contact_name: Name of contact to inspect
    """
    try:
        # Click on contact
        chat_xpath = f'//span[@title="{contact_name}"]'
        chat = driver.find_element(By.XPATH, chat_xpath)
        chat.click()
        print(f"Selected contact: {contact_name}")
        time.sleep(3)
        
        print("\n" + "=" * 60)
        print("WHATSAPP HEADER STRUCTURE ANALYSIS")
        print("=" * 60)
        
        # Get header element
        header = driver.find_element(By.XPATH, '//header')
        
        print(f"\n1. FULL HEADER TEXT:")
        print(f"   {repr(header.text)}")
        
        # Analyze spans
        print(f"\n2. SPAN ELEMENTS IN HEADER:")
        spans = header.find_elements(By.TAG_NAME, 'span')
        for i, span in enumerate(spans):
            text = span.text.strip()
            if text:
                print(f"   [{i}] '{text}'")
                try:
                    title = span.get_attribute('title')
                    if title:
                        print(f"       title='{title}'")
                except:
                    pass
        
        # Test status detection XPaths
        print(f"\n3. TESTING STATUS DETECTION:")
        test_xpaths: List[Tuple[str, str]] = [
            ('//header//span[contains(text(), "online")]', 'online'),
            ('//header//span[contains(text(), "typing")]', 'typing'),
            ('//header//span[contains(text(), "last seen")]', 'last seen'),
        ]
        
        for xpath, description in test_xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    print(f"   [OK] {description}: found")
                    for elem in elements[:2]:
                        print(f"        Text: '{elem.text.strip()}'")
                else:
                    print(f"   [--] {description}: not found")
            except Exception as e:
                print(f"   [ERR] {description}: {e}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error during inspection: {e}")
        import traceback
        traceback.print_exc()


def main() -> None:
    """Main entry point for debug script."""
    print("WhatsApp Web Debug Tool")
    print("=" * 60)
    
    # Load config if available
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
    sys.path.insert(0, config_path)
    
    try:
        import config
        contact_name = getattr(config, 'CONTACT_NAME', 'Contact Name')
    except ImportError:
        contact_name = input("Enter contact name to debug: ")
    
    chromedriver_path = get_chromedriver_path()
    driver = setup_driver(chromedriver_path)
    
    try:
        driver.get('https://web.whatsapp.com/')
        print("\nScan QR code to log in...")
        input("Press Enter once logged in...")
        
        inspect_header(driver, contact_name)
        
        input("\nPress Enter to close browser...")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
