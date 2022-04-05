#!/usr/bin/env python3

# Python DNS query client
#
# Example usage:
#   ./dns.py --type=A --name=www.pacific.edu --server=8.8.8.8
#   ./dns.py --type=AAAA --name=www.google.com --server=8.8.8.8

# Should provide equivalent results to:
#   dig www.pacific.edu A @8.8.8.8 +noedns
#   dig www.google.com AAAA @8.8.8.8 +noedns
#   (note that the +noedns option is used to disable the pseduo-OPT
#    header that dig adds. Our Python DNS client does not need
#    to produce that optional, more modern header)


from dns_tools import dns  # Custom module for boilerplate code

import argparse
import ctypes
import random
import socket
import struct
import sys


def main():
    # Setup configuration
    parser = argparse.ArgumentParser(description='DNS client for ECPE 170')
    parser.add_argument('--type', action='store', dest='qtype',
                        required=True, help='Query Type (A or AAAA)')
    parser.add_argument('--name', action='store', dest='qname',
                        required=True, help='Query Name')
    parser.add_argument('--server', action='store', dest='server_ip',
                        required=True, help='DNS Server IP')

    args = parser.parse_args()
    qtype = args.qtype
    qname = args.qname
    server_ip = args.server_ip
    port = 53
    server_address = (server_ip, port)

    if qtype not in ("A", "AAAA"):
        print("Error: Query Type must be 'A' (IPv4) or 'AAAA' (IPv6)")
        sys.exit()

    # Create UDP socket
    # ---------
    # STUDENT TO-DO
    # ---------
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(server_address)

    # Generate DNS request message
    # ---------
    # STUDENT TO-DO
    # ---------
    transaction_id = random.randint(0, (2 << 16 - 1))
    standard_query = 0x0120
    qd_count = 1
    an_count = 0
    ns_count = 0
    ar_count = 0
    message_header_bytes = struct.pack(
        ">HHHHHH",
        transaction_id,
        standard_query,
        qd_count,
        an_count,
        ns_count,
        ar_count
    )

    question_bytes = b''
    for section in qname.split('.'):
        question_bytes += len(section).to_bytes(1, 'big')
        question_bytes += bytes(section, 'ascii')
    question_bytes += (0x00).to_bytes(1, "big")

    if qtype == "A":
        qtypenum = 1
    elif qtype == "AAAA":
        qtypenum = 28
    else:
        raise Exception(f"Unknown qtype: {qtype}")
    question_bytes += qtypenum.to_bytes(2, 'big')

    qclass = 1
    question_bytes += qclass.to_bytes(2, 'big')

    request_bytes = message_header_bytes + question_bytes
    print(request_bytes)

    # Send request message to server
    # (Tip: Use sendto() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------

    s.sendto(request_bytes, server_address)

    # Receive message from server
    # (Tip: use recvfrom() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------

    raw_bytes, rec_address = s.recvfrom(1024)

    # Close socket
    # ---------
    # STUDENT TO-DO
    # ---------

    s.close()

    # Decode DNS message and display to screen
    dns.decode_dns(raw_bytes)


if __name__ == "__main__":
    sys.exit(main())
