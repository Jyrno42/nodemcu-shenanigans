import json
import socket
import struct
import re
import threading

from datetime import datetime
from time import sleep

from flask import Flask

app = Flask(__name__)

with open('multicast-dashboard.html') as h:
    html_content = h.read()

state = {
    'ip': None,
    'sensor_tick': None,
    'temperature': None,
    'humidity': None
}

@app.route('/')
def root():
    return html_content


@app.route('/api/measurements')
def measurements():
    return state


@app.route('/api/ip')
def get_ip():
    return state['ip']


@app.route('/api/ip/refresh', methods=['POST'])
def api_refresh_ip():
    state['ip'] = get_local_ip()

    return state['ip']


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def refresh_ip():
    while True:
        state['ip'] = get_local_ip()
        sleep(180)


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

            try:
                data = json.loads(data)

                try:
                    state['temperature'] = round(data['temperature'], 1)

                except (TypeError, ValueError):
                    state['temperature'] = None

                try:
                    state['humidity'] = int(data['humidity'])

                except (TypeError, ValueError):
                    state['humidity'] = 'no-value'

                state['sensor_tick'] = datetime.now().isoformat().split('.')[0]

            except (ValueError, TypeError):
                pass

    finally:
        s.close()

threading.Thread(target=run_socket).start()
threading.Thread(target=refresh_ip).start()
