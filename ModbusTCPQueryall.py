import time
import csv
from pyModbusTCP.client import ModbusClient
import pandas as pd

# Load the Excel file to read register information
file_path = 'PCS-Modbus register addr declaration-V1.12 1.xlsx'
xls = pd.ExcelFile(file_path)

# Read the relevant sheet containing input registers
input_registers_df = pd.read_excel(xls, sheet_name='Input Register(FUN CODE 04)')

# Extract the relevant columns from the spreadsheet
addresses = input_registers_df['Address (DEC)'].tolist()
meanings = input_registers_df['Meaning '].tolist()

# Modbus connection setup
slave_address = '192.168.0.232'  # Replace with actual Modbus device IP
port = 502
modbus_client = ModbusClient(host=slave_address, port=port, auto_open=True)

# CSV file setup
csv_file = "modbus_data_all_registers.csv"

# Create or open the CSV file and write the header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Adding "Register Meaning" as column header
    header = ["Timestamp"]
    for meaning in meanings:
        header.append(f"{meaning} (Value)")
    writer.writerow(header)

if __name__ == '__main__':
    while True:
        # Prepare a list to store the queried values
        register_values = [512]
        
        for address in addresses:
            # Reading each register value one by one based on the address
            reg_value = modbus_client.read_input_registers(address, 1)
            
            if reg_value:
                register_values.append(reg_value[0])  # Append the value if read successfully
            else:
                register_values.append('Error')  # Append 'Error' in case of a read failure
        
        # Get the current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the data to CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp] + register_values)
        
        print(register_values)  # Optional: Print the values for debugging

        time.sleep(2)  # Wait for 2 seconds before the next read


# Print out the column names to inspect them
#print(input_registers_df.columns)
