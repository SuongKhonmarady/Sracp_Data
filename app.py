import csv
import requests
import re
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = "https://www.wedushare.com/"  # Replace with the actual URL

# Send a GET request to the website and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing the titles and deadlines
title_elements = soup.find_all("h4", class_="!text-white font-heading text-gray line-clamp-2 group-hover:!text-yellow duration-300 transition-colors text-lg sm:text-2xl")
deadline_elements = soup.find_all("div", class_="flex flex-wrap sm:pb-6")

# Check if the lengths match
if len(title_elements) != len(deadline_elements):
    print(f"Warning: Mismatched elements! Titles: {len(title_elements)}, Deadlines: {len(deadline_elements)}")

# Create a list to store the scraped data
data = []

date_pattern = r"([A-Za-z]+ \d{1,2}, \d{4})"

# Iterate over the elements
for title_element, deadline_element in zip(title_elements, deadline_elements):
    title = title_element.text.strip()
    
    # Extract the deadline
    deadline_info = deadline_element.text.strip().lower()
    if "deadline" in deadline_info:
        match = re.search(date_pattern, deadline_info)
        deadline = match.group(0) if match else "No valid date found"
    else:
        deadline = "No deadline"
    
    data.append([title, deadline])

# Remove duplicate entries (if any)
unique_data = [list(item) for item in set(tuple(row) for row in data)]

# Export the data to a CSV file
csv_filename = "news_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Deadline"])
    writer.writerows(unique_data)

print(f"Data scraped successfully and saved to {csv_filename}.")
