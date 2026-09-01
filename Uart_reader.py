import serial
import os
import json
import time

PORT = '/dev/ttyACM0'  
BAUD_RATE = 115200

# Use absolute path to avoid directory mismatch
DATA_FOLDER = os.path.expanduser('~/data_csvs')

os.makedirs(DATA_FOLDER, exist_ok=True)

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {PORT} at {BAUD_RATE} baud...")
except serial.SerialException as e:
    print(f"Error opening port: {e}")
    exit(1)

while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8', 'ignore').strip()
        print(f"Received command from ESP32: {command}")
        
        if command == "LIST":
            # Match both .csv and .CSV
            files = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith('.csv')]
            response = json.dumps(files) + '\n'
            print(f"Sending file list: {response.strip()}")
            ser.write(response.encode('utf-8'))
            
        elif command.startswith("GET:"):
            filename = command.split(":", 1)[1]
            filepath = os.path.join(DATA_FOLDER, filename)
            print(f"Streaming file: {filepath}")
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = f.read()
                    ser.write(data.encode('utf-8'))
                    if not data.endswith('\n'):
                        ser.write(b'\n')
            
            ser.write(b'EOF_MARKER\n')
            time.sleep(0.1)
