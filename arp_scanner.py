#!/usr/bin/env python3

import argparse
import scapy.all as scapy
import sys
import signal
from termcolor import colored

def def_handler(sig, frame):
	print(colored("Saliendo!", "red"))
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
	parser = argparse.ArgumentParser(description="Mac changer")
	parser.add_argument("-t", "--target", required=True, dest="target", help="Target (IP/Range)")
	args = parser.parse_args()
	return args.target

def scan(target):
	# scapy.arping(target)
	arp_packet = scapy.ARP(pdst=target)
	broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	packet = broadcast_packet/arp_packet

	answered, unaswered = scapy.srp(packet, timeout=1, verbose=False)
	response = answered.summary()
	if response:
		print(response)
	
	sys.exit(0)

def main():
	target = get_arguments()
	scan(target)

if __name__ == "__main__":
	main()
