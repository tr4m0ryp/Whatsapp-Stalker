import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import shutil
import os
import platform
import sys

# Try to automatically locate chromedriver in PATH
CHROMEDRIVER_PATH = shutil.which("chromedriver")
if CHROMEDRIVER_PATH:
    print(f"Found chromedriver at: {CHROMEDRIVER_PATH}")
else:
    if platform.system() == "Windows":
        CHROMEDRIVER_PATH = r"C:\\path\\to\\chromedriver.exe"
    else:
        CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

    if not os.path.exists(CHROMEDRIVER_PATH):
        print("\nchromedriver not found on this system.\n")
        sys.exit(1)

CONTACT_NAME = "Moussanigger"  # Same contact as main script

service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://web.whatsapp.com/')
print("Scan the QR code to log in to WhatsApp Web.")
input("Press Enter once you are logged in...")

# Click on the contact
try:
    chat_xpath = f'//span[@title="{CONTACT_NAME}"]'
    chat = driver.find_element(By.XPATH, chat_xpath)
    chat.click()
    print(f"\n✓ Clicked on contact: {CONTACT_NAME}")
    time.sleep(3)  # Wait for chat to load

    print("\n" + "="*80)
    print("INSPECTING WHATSAPP HEADER STRUCTURE")
    print("="*80)

    # Get the entire header
    header = driver.find_element(By.XPATH, '//header')

    print(f"\n1. FULL HEADER TEXT:")
    print(f"   {repr(header.text)}")
    print(f"   Lines: {header.text.split(chr(10))}")

    # Get all spans in header
    print(f"\n2. ALL SPANS IN HEADER:")
    spans = header.find_elements(By.TAG_NAME, 'span')
    for i, span in enumerate(spans):
        text = span.text.strip()
        if text:  # Only show spans with text
            print(f"   Span {i}: '{text}'")
            # Get attributes
            try:
                class_attr = span.get_attribute('class')
                title_attr = span.get_attribute('title')
                dir_attr = span.get_attribute('dir')
                print(f"      class='{class_attr}', title='{title_attr}', dir='{dir_attr}'")
            except:
                pass

    # Get all divs in header
    print(f"\n3. ALL DIVS IN HEADER (with text):")
    divs = header.find_elements(By.TAG_NAME, 'div')
    for i, div in enumerate(divs):
        text = div.text.strip()
        if text and len(text) < 100:  # Only short text divs
            print(f"   Div {i}: '{text}'")

    # Try specific XPaths that might contain status
    print(f"\n4. TESTING SPECIFIC XPATHS:")

    test_xpaths = [
        ('//header//span[contains(text(), "online")]', 'Looking for "online" text'),
        ('//header//span[contains(text(), "typing")]', 'Looking for "typing" text'),
        ('//header//span[contains(text(), "last seen")]', 'Looking for "last seen" text'),
        ('//header//div[@role="button"]//following-sibling::*', 'Following contact button'),
        ('//header//div[contains(@class, "copyable-text")]', 'Copyable text divs'),
    ]

    for xpath, description in test_xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if elements:
                print(f"\n   ✓ {description} ({xpath}):")
                for elem in elements[:3]:  # Show first 3 matches
                    print(f"      Text: '{elem.text.strip()}'")
            else:
                print(f"\n   ✗ {description} - No elements found")
        except Exception as e:
            print(f"\n   ✗ {description} - Error: {e}")

    # Get the raw HTML of header (first 2000 chars)
    print(f"\n5. HEADER HTML (first 2000 chars):")
    header_html = header.get_attribute('outerHTML')
    print(header_html[:2000])

    print("\n" + "="*80)
    print("Press Ctrl+C to exit")
    print("="*80)

    input("\nPress Enter to close...")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
