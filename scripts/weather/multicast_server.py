import socket
import struct
from datetime import datetime

MCAST_GRP = '239.0.0.22'
MCAST_PORT = 3535

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("waiting for data...")

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

try:
    while True:
        data, addr = s.recvfrom(100)

        if data and data.startswith(b'MARCO'):
            node_id = data[6:].decode('utf-8')
        
            s.sendto('POLO {} {}'.format(node_id, get_local_ip()).encode('utf-8'), ('239.0.0.22', 3535))
            print(node_id)

        print(f"[{datetime.now()}] {data.decode('utf-8')}")
except KeyboardInterrupt:
    pass

s.close()
print('done')
