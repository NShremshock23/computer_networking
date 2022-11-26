from tcp_packet import TCPPacket
import socket

dst = '192.168.1.1'

pkt = TCPPacket(
    '192.168.1.42',
    20,
    dst,
    666,
    b'Hello World',
    0b000101001  # Merry Christmas!
)

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
pkt_built = pkt.build()
print(pkt_built)
s.sendto(pkt_built, (dst, 0))