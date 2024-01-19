#!/usr/bin/env python3

import argparse
import scapy.all as scapy

domains_seen = set()
excluded_domains = ["google", "cloud"]

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Interface to sniff on")
    options = parser.parse_args()
    return options.interface

def process_packet(packet):
    if packet.haslayer(scapy.DNSRR):
        domain = packet[scapy.DNSQR].qname.decode()
        if not any(keyword in domain for keyword in excluded_domains):
            print(domain)
            domains_seen.add(domain)

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)

def main():
    interface = get_arguments()
    sniff(interface)

if __name__ == "__main__":
    main()
