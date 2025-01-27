import requests
import json

# === Configuration ===
ACCESS_TOKEN = "EABw2c6zKclUBO5sIFzhAfgyvXcY48nWDCAxLeiBUfYCHRILrBB0ylurfR4ns0uSIBFb1tKMIe7MZBIzgD2KEiRlehenpTJzpZBSU8cj0ywCTTK7SnUYH70B1PZCCeLiRQ8JHrnDiZAAeN8SapWGJPwIfoxXBPgDlAqZA6C5808jpUjZCH7kZCI7wehRQ4YtZCWfN"  # Replace with your Facebook Graph API access token
PAGE_ID = "ScholarshipUYFCPP"  # Replace with the Facebook Page ID or username
FIELDS = "message,created_time,id"  # Fields to retrieve (customize as needed)
OUTPUT_FILE = "facebook_data.json"  # File to save the data

# === API Endpoint ===
GRAPH_API_URL = f"https://graph.facebook.com/v15.0/{PAGE_ID}/posts"

# === Parameters for the API call ===
params = {
    "access_token": ACCESS_TOKEN,
    "fields": FIELDS
}

# === Function to Fetch Data ===
def fetch_facebook_data():
    try:
        # Send GET request to Facebook Graph API
        response = requests.get(GRAPH_API_URL, params=params)
        
        # Check for errors in the response
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            return None

        # Parse and return the JSON data
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# === Function to Save Data to JSON File ===
def save_data_to_file(data):
    try:
        with open(OUTPUT_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# === Main Script ===
if __name__ == "__main__":
    print("Fetching Facebook Page data...")
    data = fetch_facebook_data()

    if data:
        print("Data fetched successfully!")
        save_data_to_file(data)
        print("Here is a summary of the posts:")
        for post in data.get("data", []):
            print(f"Post ID: {post.get('id')}")
            print(f"Message: {post.get('message')}")
            print(f"Created Time: {post.get('created_time')}")
            print("-" * 50)
    else:
        print("Failed to fetch data.")
