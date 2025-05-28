from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Scrape import StockInformation
import time

service = Service(executable_path="chromedriver2.exe")

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("--start-maximized")  # Open in maximized window
options.add_argument("--disable-infobars")  # Removes "Chrome is being controlled" message
options.add_argument("--disable-popup-blocking")  # Prevents popups
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

company_name = ["TATACOMM"]

for name in company_name:
    time.sleep(2)
    print(f"Scrapping Information of {name} \n")
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={name}"
    driver.get(url)
    time.sleep(5)

    # Scrape Data
    scraper = StockInformation(driver)
    #scraper.fetch_dividends(name)
    #scraper.fetch_events(name)
    scraper.fetch_stock_price_3m(name)
    #scraper.fetch_stock_price_1d(name)

driver.quit()
