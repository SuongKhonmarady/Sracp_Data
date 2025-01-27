import csv
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from urllib.parse import urljoin  # To handle relative URLs

# === Selenium Setup ===
driver_path = "chromedriver.exe"  # Replace with the path to your ChromeDriver
FB_PAGE_URL = "https://www.wedushare.com/search"  # Target URL
# FB_PAGE_URL = "https://www.wedushare.com/"  # Target URL

# Start Selenium WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(FB_PAGE_URL)

# Wait for content to load
time.sleep(5)

# Scroll to load more posts dynamically
body = driver.find_element(By.TAG_NAME, "body")
for _ in range(10):  # Adjust the number of scrolls as needed
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Get the page source after scrolling
page_source = driver.page_source

# Close the browser
driver.quit()

# === BeautifulSoup Parsing ===
# Use the page source obtained from Selenium
soup = BeautifulSoup(page_source, "html.parser")

# Base URL for constructing full links
base_url = "https://www.wedushare.com"

# Find elements for titles (splitting class content)
title_elements = soup.find_all("h2", class_="font-heading text-base 2xl:text-lg line-clamp-2")

# Find the deadline elements within the class "space-y-2"
deadline_elements = soup.find_all("div", class_="space-y-2")

# Create a list to store scraped data
data = []

# Regular expression for extracting date in a format like: 'November 09, 2026'
date_pattern = r"([A-Za-z]+ \d{1,2}, \d{4})"

# Iterate over titles and deadlines to extract data
for title_element, deadline_element in zip(title_elements, deadline_elements):
    # Extract the title text
    title = title_element.text.strip()

    # Check for deadline within the "space-y-2" div
    deadline_info = deadline_element.text.strip().lower()
    
    # If "deadline" is found, extract the date using regex
    if "deadline" in deadline_info:
        match = re.search(date_pattern, deadline_info)
        if match:
            deadline = match.group(0)  # Get the matched date
        else:
            deadline = "No valid date found"
    else:
        deadline = "No deadline"

    # Extract link
    link_tag = title_element.find_parent("a")  # Find the parent <a> tag of the title
    full_link = urljoin(base_url, link_tag["href"]) if link_tag and link_tag["href"] else "No link found"

    # Append data to the list
    data.append([title, deadline, full_link])

# === Save Data to CSV ===
csv_filename = "Scraped_data_from_wedushare.csv"  # Specify desired filename
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Deadline", "Link"])  # Write header row
    writer.writerows(data)  # Write data rows

print(f"Data scraped successfully and saved to {csv_filename}.")
