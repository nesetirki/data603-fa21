import time
import socket

import requests

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 22225        # Port to listen on (non-privileged ports are > 1023)

elapsed = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while elapsed < 60:
            data = requests.get('http://api.open-notify.org/iss-now.json').text
            conn.sendall(str.encode(data+'\n'))
            delay = 4
            elapsed += delay
            time.sleep(delay)
