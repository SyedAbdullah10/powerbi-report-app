from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

reports = [
    {
        "folder": "UDT-Dashboard",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiN2Q1MmE2NjAtOTdhZS00ZTk3LWJlOGMtMzUwNmI0YmQzNTJjIiwidCI6ImY2MzFmNGVmLWMzYmItNDU5OC04NWZmLTM2OTNlNzZmMmZmYiIsImMiOjZ9"
    },
    # {
    #     "folder": "report2",
    #     "url": "https://app.powerbi.com/view?r=eyJrIjoiXYZ..."
    # }
]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')

for report in reports:
    folder_path = os.path.join("public", report["folder"])
    os.makedirs(folder_path, exist_ok=True)
    output_path = os.path.join(folder_path, "report.pdf")
    chrome_options.add_argument(f'--print-to-pdf={output_path}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(report["url"])
    time.sleep(15)
    driver.execute_script("window.print();")
    time.sleep(3)
    driver.quit()

    print(f"✅ PDF saved: {output_path}")
