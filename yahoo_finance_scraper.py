from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pandas as pd
import time

# Tickers to scrape
TICKERS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']

def get_driver():
    ua = UserAgent()
    user_agent = ua.random

    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    return driver

def scrape_summary_ul(driver, ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    driver.get(url)
    time.sleep(2)  # Give time to load content

    data = {"Ticker": ticker}
    try:
        ul = driver.find_element(By.XPATH, '//ul[contains(@class, "yf-1jj98ts")]')
        list_items = ul.find_elements(By.TAG_NAME, 'li')

        for li in list_items:
            try:
                label_el = li.find_element(By.CLASS_NAME, 'label')
                value_el = li.find_element(By.CLASS_NAME, 'value')

                label = label_el.text.strip()
                value = value_el.text.strip()

                data[label] = value
            except Exception:
                continue
    except Exception as e:
        print(f"[{ticker}] Error: {e}")
        return None

    return data

def main():
    driver = get_driver()
    all_data = []

    for ticker in TICKERS:
        print(f"Scraping {ticker}...")
        info = scrape_summary_ul(driver, ticker)
        if info:
            all_data.append(info)
        else:
            print(f"{ticker} failed to fetch.")

    driver.quit()

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel("yahoo_finance_data.xlsx", index=False)
        print("\n✅ Data saved to 'yahoo_finance_data.xlsx'")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
