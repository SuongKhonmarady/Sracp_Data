from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# === Setup WebDriver ===
driver_path = "chromedriver.exe"  # Replace with the path to your ChromeDriver
FB_PAGE_URL = "https://www.wedushare.com/search"

# Start the browser
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(FB_PAGE_URL)

# Wait for content to load
time.sleep(5)

# Scroll to load more posts
body = driver.find_element(By.TAG_NAME, "body")
for _ in range(3):  # Scroll 3 times
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Extract post data
posts = driver.find_elements(By.CLASS_NAME, "du4w35lb")  # Find elements (class name may vary)
print(f"Found {len(posts)} posts.")

for idx, post in enumerate(posts, 1):
    print(f"Post {idx}: {post.text[:100]}...")  # Truncate content for display

# Close the browser
driver.quit()
