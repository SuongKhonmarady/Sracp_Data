import csv
from datetime import datetime, timedelta

# Define the input and output CSV file names
input_filename = "Scraped_data_from_wedushare.csv"
output_filename = "data_modified2.csv"

# Open the original CSV file
with open(input_filename, "r", newline="", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)  # Read the header row
    data = list(reader)    # Read all the data

# Ensure required columns exist
required_columns = ["Description", "Deadline", "Link"]
for col in required_columns:
    if col not in header:
        raise ValueError(f"The '{col}' column is missing from the CSV file.")

# Get indexes of the necessary columns
description_index = header.index("Description")
deadline_index = header.index("Deadline")
link_index = header.index("Link")

# Remove "Post_At" if it exists, as we will reposition it
if "Post_At" in header:
    header.remove("Post_At")

# Insert "Post_At" right after "Description"
header.insert(description_index + 1, "Post_At")

# Define the date format
date_format = "%Y-%m-%d"

# Process each row to adjust the Deadline format and set Post_At
new_data = []
for row in data:
    deadline = row[deadline_index].strip() if len(row) > deadline_index else ""

    # Ensure row has enough columns before modifying
    while len(row) < len(header):
        row.append("")

    # Fix Post_At calculation
    if deadline.lower() == "null" or not deadline:
        row[deadline_index] = "null"
        row.insert(description_index + 1, "null")  # Insert Post_At after Description
    else:
        try:
            # Parse the deadline (assuming format: "Month DD, YYYY")
            deadline_date = datetime.strptime(deadline, "%B %d, %Y")
            
            # Format Deadline as YYYY-MM-DD
            row[deadline_index] = deadline_date.strftime(date_format)

            # Set Post_At to one month before the deadline
            post_at_date = deadline_date - timedelta(days=30)
            post_at_formatted = post_at_date.strftime(date_format)

            # Insert Post_At after Description
            row.insert(description_index + 1, post_at_formatted)

        except ValueError:
            row[deadline_index] = "null"
            row.insert(description_index + 1, "null")  # Insert null for Post_At if parsing fails

    # Ensure Link is not overwritten with null
    row[link_index] = row[link_index] if row[link_index].strip() else "null"

    # Add the modified row to new_data
    new_data.append(row)

# Write the modified data to a new CSV file
with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)  # Write the modified header row
    writer.writerows(new_data)  # Write the modified data rows

print(f"Data with fixed Post_At and Link has been saved to {output_filename}.")
