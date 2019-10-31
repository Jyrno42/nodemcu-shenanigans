import atexit
import json
import socket
import struct
import re
import threading
import traceback

from datetime import datetime
from time import sleep

from flask import Flask, abort, jsonify, render_template, request

state = {
    'ip': None,
    'temperature': None,
    'moisture': 'no-value',
    'humidity': 'no-value'
}

POOL_TIME = 5

data_lock = threading.Lock()
ip_thread = threading.Thread()
socket_thread = threading.Thread()


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

        if state['ip'] == '127.0.0.1':
            sleep(10)

        else:
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
            data = s.recv(100)

            if data and data.startswith(b'MARCO'):
                node_id = data[6:].decode('utf-8')
            
                s.sendto('POLO {} {}'.format(node_id, get_local_ip()).encode('utf-8'), ('239.0.0.22', 3535))

    finally:
        s.close()


def create_app():
    app = Flask(__name__)

    def start():
        global ip_thread
        global socket_thread

        ip_thread = threading.Thread(target=refresh_ip)
        socket_thread = threading.Thread(target=run_socket)

        ip_thread.start()
        socket_thread.start()

    start()

    return app

app = create_app()


@app.route('/')
def root():
    return render_template('multicast-dashboard.html')


@app.route('/api/measurements')
def measurements():
    return state


@app.route('/api/ip')
def get_ip():
    return state['ip']


@app.route('/api/status')
def status():
    return jsonify({
        'name': 'probe-controller.local'
    }), 200


@app.route('/api/ip/refresh', methods=['POST'])
def api_refresh_ip():
    state['ip'] = get_local_ip()

    return state['ip']


@app.route('/api/temperature', methods=['POST'])
def api_update_temperature():
    value = request.json.get('value', None)
    timestamp = request.json.get('timestamp', None)

    if value is None or timestamp is None:
        return abort(400)

    try:
        value = round(float(value), 1)

    except:
        traceback.print_exc()
        return abort(400)

    state['temperature'] = [timestamp, value]

    return jsonify({'temperature': state['temperature']}), 200


@app.route('/api/humidity', methods=['POST'])
def api_update_humidity():
    value = request.json.get('value', None)
    timestamp = request.json.get('timestamp', None)

    if value is None or timestamp is None:
        return abort(400)

    try:
        value = int(value)

    except:
        traceback.print_exc()
        return abort(400)

    state['humidity'] = [timestamp, value]

    return jsonify({'humidity': state['humidity']}), 200


@app.route('/api/moisture', methods=['POST'])
def api_update_moisture():
    value = request.json.get('value', None)
    timestamp = request.json.get('timestamp', None)

    if value is None or timestamp is None:
        return abort(400)

    try:
        value = round(float(value), 1)

    except:
        traceback.print_exc()
        return abort(400)

    state['moisture'] = [timestamp, value]

    return jsonify({'moisture': state['moisture']}), 200
