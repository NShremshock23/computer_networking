import socket
import struct
import array

def chksum(packet):
    """
    :param packet: packet after being built using struct:
    This function calculates the checksum for TCP packet passed to it.
    It checks for lengths of 16 and then calculates the checksum.
    This code was created looking throught the source code of Scapy and how
    Scapy finds the checksum.
    """
    if len(packet) % 2 != 0: # check length of the packet
        packet += b'\0'
    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff

class TCPPacket:
    def __init__(self,
                 src_host, # Source IP
                 src_port, # Source Port
                 dst_host, # Destination IP
                 dst_port, # Destination Port
                 data, # Message to be sent
                 flags=0):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.data = data
        self.flags = flags

    def build(self):
        """
        This function takes the values used to initialize the class and 
        then with default values packs them into a binary structure using struct.
        A packet and psuedo header are created then a checksum is calculated and added.
        returns the built packet with the checksum
        """
        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            0,              # Sequence Number
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),    # Source Address
            socket.inet_aton(self.dst_host),    # Destination Address
            socket.IPPROTO_TCP,                 # Protocol ID
            len(packet)                         # TCP Length
        )

        # calculate the checksum and then pack it using struct.
        # add the checksum with the packet and the data
        checksum = chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
        packet = packet + self.data
        return packet
