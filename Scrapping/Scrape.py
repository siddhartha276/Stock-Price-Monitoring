import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from add_to_mongo import AddData

add_data = AddData()

today = date.today().strftime("%d-%m-%Y")

class StockInformation:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def fetch_dividends(self, company_name):
        try:
            corporate_actions = self.wait.until(EC.element_to_be_clickable((By.ID, "corporateActions")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", corporate_actions)
            time.sleep(random.uniform(2, 4))
            self.driver.execute_script("arguments[0].click();", corporate_actions)

            self.wait.until(lambda driver: "active show" in driver.find_element(By.ID, "Corporate_Actions").get_attribute("class"))
            corp_action_table = self.wait.until(EC.visibility_of_element_located((By.ID, "corpActionTable")))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", corp_action_table)
            time.sleep(random.uniform(2, 4))

            table = corp_action_table.find_element(By.TAG_NAME, "table")
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            header = table.find_element(By.TAG_NAME, "thead")
            header_row = header.find_element(By.TAG_NAME, "tr").text
            lines = [header_row]

            if not rows:
                print("No dividend data found.")
                return

            print("\nDividend Data:\n")
            for row in rows:
                line = row.text
                lines.append(line)
                print(line)

            with open(f"../ScrappedData/{company_name}_dividends.txt", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

        except Exception as e:
            print(f"Error fetching dividends: {e}")

    def fetch_events(self, company_name):
        try:
            event_calendar = self.wait.until(EC.element_to_be_clickable((By.ID, "eventcalender")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", event_calendar)
            time.sleep(random.uniform(2, 5))
            self.driver.execute_script("arguments[0].click();", event_calendar)

            corp_event_table = self.wait.until(EC.presence_of_element_located((By.ID, "corpEventCalenderTable")))
            self.wait.until(lambda driver: corp_event_table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr"))
            time.sleep(random.uniform(2, 5))

            table = corp_event_table.find_element(By.TAG_NAME, "table")
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            header = table.find_element(By.TAG_NAME, "thead")
            header_row = header.find_element(By.TAG_NAME, "tr").text
            lines = [header_row]

            if not rows:
                print("No event data found.")
                return

            print("\nEvent Calendar Data:\n")

            for row in rows:
                line = row.text
                lines.append(line)
                print(line)

            with open(f"../ScrappedData/{company_name}_events.txt", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

        except Exception as e:
            print(f"Error fetching events: {e}")

    def fetch_stock_price_3m(self, company_name):
        try:

            historical_data_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#info-historicaldata']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",historical_data_button)

            time.sleep(random.uniform(2, 4))
            self.driver.execute_script("arguments[0].click();", historical_data_button)

            historical_trade = self.wait.until(EC.presence_of_element_located((By.ID, "historical-trade")))
            time.sleep(random.uniform(2, 4))

            # Click on the 3-month filter
            three_months_button = self.wait.until(EC.element_to_be_clickable((By.ID, "threeM")))
            self.driver.execute_script("arguments[0].click();", three_months_button)
            time.sleep(random.uniform(2, 4))

            # Click on the filter button
            filter_button = self.wait.until(EC.element_to_be_clickable((By.ID, "tradeDataFilter")))
            self.driver.execute_script("arguments[0].click();", filter_button)
            time.sleep(random.uniform(2, 4))

            # Wait for table to appear
            equity_historical_table = self.wait.until(
                EC.visibility_of_element_located((By.ID, "equityHistoricalTable")))
            body = equity_historical_table.find_element(By.TAG_NAME, "tbody")
            rows = body.find_elements(By.TAG_NAME, "tr")  # FIXED: find **all** rows

            if not rows:
                print("No 3-month historical data found.")
                return

            # Print historical data
            lines = []
            print("\n3-month historical data:\n")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 14:
                    continue  # skip incomplete rows

                add_data.append_data(cells, company_name)

                date_col = cells[0].text
                open_price = cells[2].text
                high = cells[3].text
                low = cells[4].text
                prev_close = cells[5].text
                close = cells[7].text
                volume = cells[11].text
                value = cells[12].text
                trades = cells[13].text

                line = (
                    f"On {date_col}, {company_name}'s stock opened at {open_price}, reached a high of {high} "
                    f"and a low of {low}. The previous day's closing price was {prev_close}, and on {date_col} it closed at {close}. "
                    f"The traded volume was {volume}, with {trades} trades and total value traded was {value}.."
                )
                lines.append(line)
                print(line)

            with open(f"../ScrappedData/{company_name}_3m.txt", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

        except Exception as e:
            print(f"Error fetching the stock prices of the last 3 months: {e}")

    def fetch_stock_price_1d(self, company_name):
        try:
            historical_data_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#info-historicaldata']"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                historical_data_button
            )
            time.sleep(random.uniform(2, 4))
            self.driver.execute_script("arguments[0].click();", historical_data_button)

            historical_trade = self.wait.until(
                EC.presence_of_element_located((By.ID, "historical-trade"))
            )
            time.sleep(random.uniform(2, 4))

            # Click on the 1-day filter
            one_day_button = self.wait.until(EC.element_to_be_clickable((By.ID, "oneD")))
            self.driver.execute_script("arguments[0].click();", one_day_button)
            time.sleep(random.uniform(2, 4))

            # Click on the filter button
            filter_button = self.wait.until(EC.element_to_be_clickable((By.ID, "tradeDataFilter")))
            self.driver.execute_script("arguments[0].click();", filter_button)
            time.sleep(random.uniform(2, 4))

            # Wait for table to appear
            equity_historical_table = self.wait.until(
                EC.visibility_of_element_located((By.ID, "equityHistoricalTable"))
            )
            body = equity_historical_table.find_element(By.TAG_NAME, "tbody")
            rows = body.find_elements(By.TAG_NAME, "tr")

            if not rows:
                print("No 1-day historical data found.")
                return

            lines = []
            print("\n1-day historical data:\n")
            for row in rows:

                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 14:
                    continue  # Skip malformed rows

                add_data.append_data(cells, company_name)

                date = cells[0].text
                open_price = cells[2].text
                high = cells[3].text
                low = cells[4].text
                prev_close = cells[5].text
                close = cells[7].text
                volume = cells[11].text
                value = cells[12].text
                trades = cells[13].text

                line = (
                    f"On {date}, {company_name}'s stock opened at {open_price}, reached a high of {high} "
                    f"and a low of {low}. The previous day's closing price was {prev_close}, and on {date} it closed at {close}. "
                    f"The traded volume was {volume}, with {trades} trades and total value traded was {value}."
                )
                lines.append(line)
                print(line)

            with open(f"../ScrappedData/{company_name}_{today}.txt", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

        except Exception as e:
            print(f"Error fetching the stock prices of the last 1 day: {e}")

