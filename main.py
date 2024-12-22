import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = r"C:\path\to\chromedriver.exe" #here your chromedriver path
CONTACT_NAME = "contact_name" #here the person you would love to stalk
CHECK_INTERVAL = 5

csv_file = 'status_log.csv'
df = pd.DataFrame(columns=["Timestamp", "Status"])
df.to_csv(csv_file, index=False)

def get_contact_status(driver, contact_name):
    try:
        chat_xpath = f'//span[@title="{contact_name}"]'
        chat = driver.find_element(By.XPATH, chat_xpath)
        chat.click()

        wait = WebDriverWait(driver, 10)
        status_xpath = '//header//span[contains(text(), "online") or contains(text(), "typing...")]'
        status_element = wait.until(EC.presence_of_element_located((By.XPATH, status_xpath)))

        status_text = status_element.text.lower()
        if "online" in status_text:
            return "online"
        elif "typing" in status_text:
            return "typing..."
        else:
            return "offline"
    except (NoSuchElementException, TimeoutException):
        return "offline"

service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
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
