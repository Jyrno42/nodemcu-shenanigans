import network
import socket
import struct
import utime


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

    return sock


def write(sock, data):
    buf = data.encode('utf-8')
    print("WRITE", buf)
    sock.sendto(buf, (MCAST_GRP, MCAST_PORT))


def locate_controller(node_id):
    sock = init_multicast()

    write(sock, 'MARCO {}'.format(node_id))

    buf, addr = sock.recvfrom(100)

    print('recv', buf)

    if buf.startswith('POLO {}'.format(node_id).encode('utf-8')):
        print('found addr', buf, addr)

    