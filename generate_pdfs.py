import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import base64

# === Setup Logging ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/run.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

reports = [
    {
        "folder": "UDT-Dashboard",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiN2Q1MmE2NjAtOTdhZS00ZTk3LWJlOGMtMzUwNmI0YmQzNTJjIiwidCI6ImY2MzFmNGVmLWMzYmItNDU5OC04NWZmLTM2OTNlNzZmMmZmYiIsImMiOjZ9"
    }
]

for report in reports:
    try:
        folder_path = os.path.join("public", report["folder"])
        os.makedirs(folder_path, exist_ok=True)
        output_path = os.path.join(folder_path, "report.pdf")

        logging.info(f"🧭 Generating PDF for: {report['url']}")
        logging.info(f"📁 Saving to: {output_path}")

        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(report["url"])
        logging.info("⏳ Waiting for dashboard to fully load...")
        time.sleep(25)

        logging.info("🖨️ Exporting to PDF via DevTools...")
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "landscape": False
        })

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(pdf['data']))

        driver.quit()

        logging.info(f"✅ PDF saved successfully at: {output_path}")

    except Exception as e:
        logging.error(f"❌ Failed to generate PDF for {report['folder']}: {str(e)}")
