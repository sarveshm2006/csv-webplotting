import serial
import os
import json
import time

PORT = '/dev/ttyACM0'  
BAUD_RATE = 115200
DATA_FOLDER = './data_csvs'

os.makedirs(DATA_FOLDER, exist_ok=True)

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {PORT} at {BAUD_RATE} baud...")
except serial.SerialException as e:
    print(f"Error opening port: {e}")
    print("Tip: You may need to add your user to the 'dialout' group.")
    exit(1)

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
            time.sleep(0.1)
