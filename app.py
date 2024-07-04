from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def search_products(keywords):
    driver.get("https://www.amazon.co.uk")
    wait = WebDriverWait(driver, 20)
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
    except TimeoutException:
        print("Search box not found, using alternative method.")
        search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.nav-input[type='text']")))
    search_box.clear()
    search_box.send_keys(keywords)
    search_box.send_keys(Keys.RETURN)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot.s-result-list.s-search-results.sg-row')))

def scrape_product_details():
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
    )
    product_details = []

    for product in products:
        title = product.find_element(By.XPATH, './/h2/a/span').text
        try:
            price = product.find_element(By.XPATH, ".//span[contains(@class, 'a-price-whole')]").text
        except NoSuchElementException:
            price = "N/A"
        

        product_details.append({
            'title': title,
            'price': price,
        })

    return product_details

search_products("mobile phones")
details = scrape_product_details()
df = pd.DataFrame(details)
df.to_csv('Amazon_Product_Details.csv', index=False)
print("Data saved to 'Amazon_Product_Details.csv'.")
driver.quit()












# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pandas as pd

# # Set up the WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument('--incognito')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def search_products(keywords):
#     # Navigate to Amazon.co.uk
#     driver.get("https://www.amazon.co.uk")
#     time.sleep(2)  # Allow the page to load


#     # Locate the search box and search for the keywords
#     search_box = driver.find_element(By.ID, "twotabsearchtextbox")
#     search_box.clear()
#     search_box.send_keys(keywords)
#     search_box.send_keys(Keys.RETURN)
#     time.sleep(2)  # Allow search results to load

# def scrape_product_details():
#     # Find all product listings on the current page
#     products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

#     product_details = []

#     for product in products:
#         # Extract details from each product listing
#         title = product.find_element(By.XPATH, './/h2/a/span').text
#         try:
#             price = product.find_element(By.XPATH, './/span[@class="a-price"]/span[1]/span[2]').text
#         except:
#             price = "N/A"
#         try:
#             rating = product.find_element(By.XPATH, './/span[@aria-label]/span').text
#         except:
#             rating = "No rating"

#         product_details.append({
#             'title': title,
#             'price': price,
#             'rating': rating
#         })

#     return product_details

# # Example usage
# search_products("mobile")
# details = scrape_product_details()
# print(details)

# df = pd.DataFrame(details)

# # Save the DataFrame to a CSV file
# df.to_csv('Amazon_Product_Details.csv', index=False)

# print("Data saved to 'Amazon_Product_Details.csv'.")

# # Clean up
# driver.quit()