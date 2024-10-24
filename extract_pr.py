import csv
import json
from datetime import datetime

# Path to the local JSON file
JSON_FILE_PATH = "raw/test.json"  # Replace with your actual file path

def extract_json_to_csv(data):
    '''Function to extract specific data (closed pull requests) and write to CSV'''
    data = json.loads(data)
    
    # Prepare list to hold the rows for the CSV file
    rows = []

    # Loop through the sources in the data
    for source in data.get("Sources", []):
        # Check if the source is a pull request and "ClosedAt" is not null
        if source.get("Type") == "pull request" and source.get("ClosedAt") is not None:
            # Extract relevant fields
            title = source.get("Title", "N/A")
            created_at = source.get("CreatedAt", "N/A")
            closed_at = source.get("ClosedAt", "N/A")

            # Convert the created_at and closed_at strings to datetime objects
            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            closed_at_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")

            # Calculate the time difference
            time_lapsed = closed_at_dt - created_at_dt

            # Extract the number of prompts from the "ChatgptSharing" section
            chatgpt_sharing = source.get("ChatgptSharing", [])
            for item in chatgpt_sharing:
                number_of_prompts = item.get("NumberOfPrompts", "N/A")

                # Add the extracted data to the rows list
                rows.append([title, created_at, closed_at, time_lapsed, number_of_prompts])

    # Write the extracted data to a CSV file
    with open("closed_pull_requests_with_time_lapsed.csv", "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(["Title", "CreatedAt", "ClosedAt", "TimeLapsed", "NumberOfPrompts"])
        # Write the data rows
        csv_writer.writerows(rows)

# Read the JSON data from a local file
with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
    json_data = file.read()
    extract_json_to_csv(json_data)

print("CSV file with time lapsed has been created successfully.")
