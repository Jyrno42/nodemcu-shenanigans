import socket
import struct
import re
import threading

from flask import Flask

app = Flask(__name__)

with open('multicast-dashboard.html') as h:
    html_content = h.read()

state = {
    'temperature': None,
    'humidity': None
}

@app.route('/')
def root():
    return html_content


@app.route('/api/measurements')
def measurements():
    return {
        'temperature': state['temperature'],
        'humidity': state['humidity'],
    }


def run_socket():
    MCAST_GRP = '239.0.0.22'
    MCAST_PORT = 3535

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data = s.recvfrom(100)[0]
            data = data.decode('utf-8')

            m = re.match(r'Temperature: (\d+) and Humidity: (\d+)%', data)

            if m:
                if m.group(1):
                    state['temperature'] = int(m.group(1))

                if m.group(2):
                    state['humidity'] = int(m.group(2))

    finally:
        s.close()

thread = threading.Thread(target=run_socket)
thread.start()
