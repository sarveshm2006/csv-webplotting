

import serial
import os
import json
import time

COM_PORT = 'COM3'  # Update to your ESP32's port (e.g., /dev/ttyUSB0)
BAUD_RATE = 115200
DATA_FOLDER = './data_csvs'

os.makedirs(DATA_FOLDER, exist_ok=True)
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)

while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8').strip()
        
        if command == "LIST":
            files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
            response = json.dumps(files) + '\n'
            ser.write(response.encode('utf-8'))
            
        elif command.startswith("GET:"):
            filename = command.split(":", 1)[1]
            filepath = os.path.join(DATA_FOLDER, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = f.read()
                    ser.write(data.encode('utf-8'))
                    if not data.endswith('\n'):
                        ser.write(b'\n')
            
            ser.write(b'EOF_MARKER\n')
            time.sleep(0.1) # Small buffer delay
