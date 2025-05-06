from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

def extract_section(soup, keywords):
    """Extract text that comes after a heading containing any of the keywords."""
    for tag in soup.find_all(["h2", "h3", "strong", "b"]):
        if any(word in tag.get_text(strip=True).lower() for word in keywords):
            content = []
            next_tag = tag.find_next_sibling()
            while next_tag and next_tag.name in ["p", "ul"]:
                content.append(next_tag.get_text(strip=True))
                next_tag = next_tag.find_next_sibling()
            return "\n".join(content)
    return ""
def extract_description(content_div):
    """Extracts main description before any of the key headings."""
    description = []
    for tag in content_div.find_all(recursive=False):
        if tag.name in ["h2", "h3", "strong", "b"]:
            break  # Stop at the first heading
        if tag.name in ["p", "ul"]:
            description.append(tag.get_text(strip=True))
    return "\n".join(description)


# Setup browser
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load tag page
base_url = "https://scholarshipscorner.website/chinese-government-scholarship/"
driver.get(base_url)
time.sleep(3)

# Get links
post_elements = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title a")
post_links = [elem.get_attribute("href") for elem in post_elements]
print(f"Found {len(post_links)} posts.")

# Setup CSV
csv_file = open("chinese_scholarships_detailed.csv", mode="w", newline="", encoding="utf-8")
csv_writer = csv.DictWriter(csv_file, fieldnames=[
    "Title", "Description", "Link", "Official Link", "Deadline", "Eligibility",
    "Host Country", "Host University", "Program Duration", "Degree Offered"
])

csv_writer.writeheader()

# Loop through each post
for link in post_links:
    driver.get(link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Title
    title = soup.find("h1", class_="entry-title").text.strip()

    # Content area
    content_div = soup.find("div", class_="entry-content")

    # Official Link
    official_link = ""
    for a in content_div.find_all("a"):
        if "official" in a.text.lower() or "apply" in a.text.lower():
            official_link = a.get("href")
            break

    # Extract sections
    deadline = extract_section(content_div, ["deadline", "last date"])
    description = extract_description(content_div)
    eligibility = extract_section(content_div, ["eligibility", "who can apply", "eligible"])
    host_country = extract_section(content_div, ["host country", "study in"])
    host_university = extract_section(content_div, ["host university", "offered by"])
    program_duration = extract_section(content_div, ["program duration", "duration"])
    degree_offered = extract_section(content_div, ["degree", "degree offered", "field of study", "what you will study"])

    # Save
    csv_writer.writerow({
    "Title": title,
    "Description": description,
    "Link": link,
    "Official Link": official_link,
    "Deadline": deadline,
    "Eligibility": eligibility,
    "Host Country": host_country,
    "Host University": host_university,
    "Program Duration": program_duration,
    "Degree Offered": degree_offered,
    
})



    print(f"✅ Saved: {title}")

# Done
csv_file.close()
driver.quit()
print("🎉 Data saved to chinese_scholarships_detailed.csv")
