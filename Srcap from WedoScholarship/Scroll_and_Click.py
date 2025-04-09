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
FB_PAGE_URL = "https://www.wedushare.com/"  # Target URL

# Start Selenium WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(FB_PAGE_URL)

# Wait for the initial page to load
time.sleep(5)

# Scroll and click the "Show More" button
try:
    for _ in range(10):  # Adjust the number of scroll attempts as needed
        # Scroll the page
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

        # Try to find and click the "Show More" button
        try:
            show_more_button = driver.find_element(By.XPATH, "//button[contains(@class, 'font-semibold border disabled:opacity-65 disabled:pointer-events-none text-base py-2 lg:py-4 px-4 lg:px-8 rounded-full shadow text-white bg-orange-500 border-transparent hover:bg-orange-500/90') and contains(@class, 'font-semibold border disabled:opacity-65 disabled:pointer-events-none text-base py-2 lg:py-4 px-4 lg:px-8 rounded-full shadow text-white bg-orange-500 border-transparent hover:bg-orange-500/90')]")
            if show_more_button.is_displayed() and show_more_button.is_enabled():
                show_more_button.click()
                print("Clicked 'Show More' button.")
                time.sleep(3)  # Wait for content to load after clicking
        except Exception:
            print("No 'Show More' button found or clickable.")
            # Continue scrolling even if the button isn't found
            continue
except Exception as e:
    print(f"Error during scrolling or button clicking: {e}")

# Get the page source after scrolling and clicking
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

link_elements = soup.find_all("a", href=True)  # Finds all <a> tags with href attributes

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
csv_filename = "scholarship_data_from_wedushare.csv"  # Specify desired filename
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Deadline", "Link"])  # Write header row
    writer.writerows(data)  # Write data rows

print(f"Data scraped successfully and saved to {csv_filename}.")
