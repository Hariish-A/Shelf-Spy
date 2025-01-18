import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = 'D:/Official/Practice/web-scraping/chromedriver-win64/chromedriver.exe'
HOMEPAGE = "http://books.toscrape.com"


def get_data(url, categories):
    from selenium.webdriver.chrome.service import Service
    
    browser_options = ChromeOptions()
    browser_options.headless = True
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--disable-dev-shm-usage')

    # Initialize WebDriver with Service
    service = Service(CHROME_DRIVER_PATH)
    driver = Chrome(service=service, options=browser_options)
    driver.get(url)
    WebDriverWait(driver, 10)

    data = []
    try:
        for category in categories:
            try:
                # Find and click the category link
                category_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//a[contains(text(), "{category}")]'))
                )
                category_element.click()

                # Scrape books in the category
                books = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product_pod'))
                )
                for book in books:
                    title = book.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("title")
                    price = book.find_element(By.CSS_SELECTOR, ".price_color").text
                    stock = book.find_element(By.CSS_SELECTOR, ".instock.availability").text.strip()
                    data.append({
                        'title': title,
                        'price': price,
                        'stock': stock,
                        'Category': category
                    })

                # Return to homepage
                driver.get(url)
            except Exception as e:
                print(f"Error while processing category '{category}': {e}")
    finally:
        driver.quit()

    return data

def export_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("books_exported.csv", index=False)
    print("Data exported to books_exported.csv")


def main():
    categories = ["Humor", "Art"]
    data = get_data(url=HOMEPAGE, categories=categories)
    if data:
        export_csv(data)
        print("Scraping complete.")
    else:
        print("No data scraped.")


if __name__ == '__main__':
    main()
