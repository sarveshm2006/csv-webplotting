# ESP32 Solar I-V Curve Telemetry Dashboard

This project creates a live web dashboard hosted on an ESP32 that plots solar panel I-V and P-V curves. Because the ESP32 has limited storage, it uses a Python script on your laptop to fetch `.csv` data files dynamically over the USB (UART) cable.

Here is the step-by-step guide to setting it up.

### Prerequisites

* **Hardware:** ESP32 board and a high-quality USB data cable.
* **Software:** [Thonny IDE](https://thonny.org/) installed on your computer.
* **Python Packages:** Install `pyserial` on your computer by running `pip3 install pyserial` in your terminal.

---

### Step 1: Laptop Setup (The Data Bridge)

1. Create a project folder on your computer and save `uart_bridge.py` inside it.
2. Run the script once to automatically generate the data folder:
```bash
python3 uart_bridge.py

```


3. Stop the script (`Ctrl + C`).
4. Move your solar panel `.csv` files into the newly created `~/data_csvs` folder in your home directory.

### Step 2: ESP32 Setup (The Web Server)

1. Open **Thonny** and connect to your ESP32.
2. Open `main.py`, update `WIFI_SSID` and `WIFI_PASS` with your 2.4 GHz Wi-Fi credentials, and save it directly to the **MicroPython device** (the root directory).
3. In Thonny's file explorer (bottom left), right-click the MicroPython device and select **New directory...**. Name it exactly: `data`
4. Save the `index.html` file into this new `data` folder on the ESP32.
5. Run `main.py` once in Thonny to connect to Wi-Fi. Look at the shell output and write down the assigned IP address (e.g., `192.168.1.50`).

### Step 3: Run the Dashboard

1. **CRITICAL:** Close Thonny completely. If Thonny is open, it locks the USB port, and the Python bridge will crash.
2. Open your terminal and start the bridge script:
```bash
python3 uart_bridge.py

```


3. Press the physical **EN** or **RST** button on your ESP32 board to restart it. It will silently connect to Wi-Fi and start the server.
4. Open a web browser on your laptop or phone (connected to the same Wi-Fi network) and enter the ESP32's IP address.

Select any CSV file from the sidebar to view your solar metrics!
