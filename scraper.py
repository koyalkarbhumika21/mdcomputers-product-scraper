from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

search_term = input("Enter product to search: ")

url = (
    "https://www.mdcomputers.in/"
    "?route=product/search&search=" + quote(search_term)
)

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all product links
    links = soup.select('a[href*="/product/"]')

    products = []
    seen = set()

    for link in links:
        product_url = link.get("href", "")
        name = link.get_text(" ", strip=True)

        # Only keep links related to the searched product
        if (
            search_term.lower() in name.lower()
            or search_term.lower().replace(" ", "-") in product_url.lower()
        ):
            if product_url not in seen and name:
                seen.add(product_url)

                # Find nearby price
                parent = link.parent
                price = "N/A"

                for _ in range(4):
                    if parent:
                        price_element = parent.select_one(".price")
                        if price_element:
                            price = price_element.get_text(
                                " ", strip=True
                            )
                            break
                        parent = parent.parent

                products.append((name, price, product_url))

    print("\nProducts found:\n")

    for name, price, product_url in products:
        print("Product:", name)
        print("Price:", price)
        print("URL:", product_url)
        print("-" * 60)

    print(f"\nTotal products found: {len(products)}")

finally:
    driver.quit()