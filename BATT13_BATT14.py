import time
from pyModbusTCP.client import ModbusClient

# Define device details
devices = {
    'BATT14': {'address': '192.168.91.232', 'port': 502},
    'BATT13': {'address': '192.168.0.232', 'port': 502}
}

# Create modbus clients for both devices
clients = {
    'BATT13': ModbusClient(host=devices['BATT13']['address'], port=devices['BATT13']['port'], auto_open=True),
    'BATT14': ModbusClient(host=devices['BATT14']['address'], port=devices['BATT14']['port'], auto_open=True)
}

def read_registers(client, label):
    regs = client.read_input_registers(512, 5)
    if regs:
        print(f"{label} registers: {regs}")
    else:
        print(f"{label}: read error occurred")

if __name__ == '__main__':
    while True:
        # Read and print data for BATT13
        read_registers(clients['BATT13'], 'BATT13')
        
        # Read and print data for BATT14
        read_registers(clients['BATT14'], 'BATT14')

        # Wait for 2 seconds before the next poll
        time.sleep(2)
