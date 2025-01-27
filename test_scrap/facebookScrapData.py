import requests
from bs4 import BeautifulSoup

# === URL of the Facebook page ===
FB_PAGE_URL = "https://www.facebook.com/ScholarshipUYFCPP"

# === Headers to Mimic a Real Browser ===
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# === Function to Scrape Data ===
def scrape_facebook_page(url):
    try:
        # Send a GET request to the Facebook page
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch the page: {response.status_code}")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Find all post content
        posts = soup.find_all("div", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"})  # This class may vary
        print(f"Found {len(posts)} posts.")

        # Extract and display post details
        for idx, post in enumerate(posts, 1):
            print(f"Post {idx}: {post.text.strip()[:100]}...")  # Truncate long content
    except Exception as e:
        print(f"An error occurred: {e}")

# === Main Script ===
if __name__ == "__main__":
    print("Scraping Facebook page data...")
    scrape_facebook_page(FB_PAGE_URL)
