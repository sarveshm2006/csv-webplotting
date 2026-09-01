import network
import socket
import sys
import uselect
import time

WIFI_SSID = "Svsh"
WIFI_PASS = "kkplkarur"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    
    # Fix for hardware EFUSE CRC error
    wlan.config(mac=b'\x24\x0A\xC4\x00\x11\x22')
    
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            time.sleep(0.5)
            timeout -= 1

def clear_serial_buffer():
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    while poller.poll(10):  # 10ms timeout
        sys.stdin.read(1)

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    
    while True:
        conn, addr = s.accept()
        try:
            req = conn.recv(1024).decode('utf-8')
            if not req:
                conn.close()
                continue
                
            path = req.split('\r\n')[0].split(' ')[1]
            
            if path == '/':
                with open('data/index.html', 'r') as f:
                    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                    while True:
                        chunk = f.read(1024)
                        if not chunk: break
                        conn.send(chunk)
                        
            elif path == '/list-files':
                clear_serial_buffer()
                sys.stdout.write("LIST\n")
                
                response = sys.stdin.readline()
                conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
                conn.send(response)
                
            elif path.endswith('.csv'):
                filename = path.lstrip('/')
                clear_serial_buffer()
                sys.stdout.write("GET:" + filename + "\n")
                
                conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/csv\r\n\r\n')
                
                while True:
                    line = sys.stdin.readline()
                    if "EOF_MARKER" in line or not line:
                        break
                    conn.send(line)
                    
            else:
                conn.send('HTTP/1.1 404 Not Found\r\n\r\n')
                
        except Exception:
            pass
        finally:
            conn.close()

connect_wifi()
start_server()
