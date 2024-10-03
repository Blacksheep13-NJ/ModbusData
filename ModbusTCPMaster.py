import time
from    pyModbusTCP.client import ModbusClient

slave_address = '192.168.0.232'
port = 502

modbus_client = ModbusClient(host=slave_address, port=port, auto_open=True)

if __name__ == '__main__': 
    while True: 
        regs = modbus_client.read_input_registers(512, 5)
        if regs:
            print(regs)
        else:
            print("read error occured")
            
        time.sleep(2)