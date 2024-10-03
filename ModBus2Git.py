import time
import csv
import requests
import base64  # Import to handle Base64 encoding
from pyModbusTCP.client import ModbusClient

# Modbus Client Setup
slave_address = '192.168.91.232'
port = 502
modbus_client = ModbusClient(host=slave_address, port=port, auto_open=True)

# GitHub Repository details
github_token = "y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"  # Replace with your GitHub personal access token
repo = "Blacksheep13-NJ/ModbusData"  # Replace with your repository name
branch = "main"  # or master or another branch

# CSV file setup
csv_file = "BATT014_modbus_data.csv"

# Create or open the CSV file and write the header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp"] + [f"Register_{i}" for i in range(512, 517)])  # CSV header

def upload_to_github(filepath, repo, branch, token):
    # Read the file content
    with open(filepath, 'rb') as f:
        content = f.read()

    # Encode the file content in Base64
    b64_content = base64.b64encode(content).decode("utf-8")

    # Construct the API URL for the file
    api_url = f"https://api.github.com/repos/{repo}/contents/{filepath}"
    
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # Prepare the data payload for the GitHub API
    data = {
        "message": "Add Modbus data CSV",
        "content": b64_content,
        "branch": branch
    }

    # Send the request to the GitHub API
    response = requests.put(api_url, json=data, headers=headers)

    # Handle the API response
    if response.status_code == 201:
        print("File uploaded successfully!")
    else:
        print(f"Error: {response.json()}")

if __name__ == '__main__': 
    while True: 
        regs = modbus_client.read_input_registers(512, 5)
        if regs:
            # Get the current timestamp
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            # Write the data to CSV
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp] + regs)

            print(regs)  # Optional: print the data to the console

            # Upload the file to GitHub
            upload_to_github(csv_file, repo, branch, github_token)
        else:
            print("read error occurred")

        time.sleep(2)
