import csv
from datetime import datetime

# Define the input and output CSV file names
input_filename = "scholarship_data_from_wedushare.csv"
output_filename = "data_modified1.csv"

# Open the original CSV file
with open(input_filename, "r", newline="", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)  # Read the header row
    data = list(reader)    # Read all the data

# Find the index of the "Deadline" column
deadline_index = header.index("Deadline")

# Define the date format
date_format = "%Y-%m-%d"

# Process each row to adjust the Deadline format
for row in data:
    deadline = row[deadline_index]
    if deadline.lower() == "null" or not deadline.strip():
        row[deadline_index] = "null"
    else:
        try:
            # Try to parse and reformat the deadline to the desired format
            deadline_date = datetime.strptime(deadline, "%B %d, %Y")  # Adjust if necessary for your format
            row[deadline_index] = deadline_date.strftime(date_format)
        except ValueError:
            row[deadline_index] = "null"  # Set to null if parsing fails

# Write the modified data to a new CSV file
with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)  # Write the header row
    writer.writerows(data)   # Write the modified data rows

print(f"Data with reformatted deadlines has been saved to {output_filename}.")
