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

try:
    while True:
        data, addr = s.recvfrom(100)

        with open('log.csv', 'a+') as h:
            h.write(f"{datetime.now()},{data.decode('utf-8')}\n")

        print(f"[{datetime.now()}] {data.decode('utf-8')}")
except KeyboardInterrupt:
    pass

s.close()
print('done')
