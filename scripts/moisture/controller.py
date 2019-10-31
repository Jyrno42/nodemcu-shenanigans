import json
import network
import select
import socket
import struct
import utime
import urequests
import os


MCAST_GRP = '239.0.0.22'
MCAST_PORT = 3535


def init_multicast():
    # Ensure AP wifi is disabled (see: https://github.com/micropython/micropython/issues/2198)
    network.WLAN(network.AP_IF).active(False)
    utime.sleep_ms(200)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    addr = socket.getaddrinfo("0.0.0.0", MCAST_PORT)[0][-1]
    sock.bind(addr)

    opt = bytes([int(x) for x in MCAST_GRP.split('.')]) + bytes([0, 0, 0, 0])
    # if there was socket.inet_pton
    #  opt =socket.inet_pton(socket.AF_INET, MULTICAST_ADDRESS) + socket.inet_pton(socket.AF_INET, "0.0.0.0")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, opt)

    sock.setblocking(0)

    return sock


def write(sock, data):
    buf = data.encode('utf-8')
    # print("WRITE", buf)
    sock.sendto(buf, (MCAST_GRP, MCAST_PORT))


def locate_controller(node_id, timeout=3):
    sock = init_multicast()

    write(sock, 'MARCO {}'.format(node_id))

    ready = select.select([sock], [], [], timeout)

    if ready[0]:
        buf, addr = sock.recvfrom(100)

        if buf.startswith('POLO {}'.format(node_id).encode('utf-8')):
            try:
                print('via multicast', addr[0])
                verify_controller(addr[0])

                return addr[0]

            except Exception as e:
                raise e

    raise Exception('Controller not found')


def verify_controller(addr):
    headers = {'content-type': 'application/json'}

    resp = urequests.get('http://{}:8000/api/status'.format(addr), headers=headers)

    if resp.status_code != 200:
        raise Exception('Bad controller found')

    if resp.json().get('name') != 'probe-controller.local':
        raise Exception('Unknown controller found')


def post_data(addr, path, data):
    headers = {'content-type': 'application/json'}

    uri = 'http://{}:8000{}'.format(addr, path)

    # print('uri', uri)

    resp = urequests.post(uri, data=json.dumps(data), headers=headers)

    if resp.status_code != 200:
        raise Exception('Failed to write data: {}'.format(resp.status_code))


def init_link(node_id):
    addr = None

    try:
        os.stat('controller.txt')

        with open('controller.txt', 'r') as h:
            addr = h.read().strip()

    except OSError:
        pass

    if addr:
        # print('via txt file', addr)

        try:
            verify_controller(addr)
            # print('via txt file: OK')

            return addr

        except:
            pass

    addr = locate_controller(node_id)

    with open('controller.txt', 'w') as h:
        # print('write to txt file', addr)
        h.write(addr)

    return addr