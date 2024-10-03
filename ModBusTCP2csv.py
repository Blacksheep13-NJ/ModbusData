import time
import csv
from pyModbusTCP.client import ModbusClient

slave_address = '192.168.91.232'
port = 502

modbus_client = ModbusClient(host=slave_address, port=port, auto_open=True)

# CSV file setup
csv_file = "BATT014_modbus_data.csv"

# Create or open the CSV file and write the header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp"] + [f"Register_{i}" for i in range(512, 517)])  # CSV header

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
        else:
            print("read error occurred")
            
        time.sleep(2)