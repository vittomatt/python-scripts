#!/usr/bin/env python3

import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

open_sockets = []

def def_handler(sig, frame):
	print(colored("Saliendo...", "red"))
	for socket in open_sockets:
		socket.close()
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def main():
	target, ports_str = get_arguments()
	ports = parse_ports(ports_str)

	with ThreadPoolExecutor(max_workers=100) as executor:
		executor.map(lambda port: scan_port(port, host), ports)

def get_arguments():
	parser = argparse.ArgumentParser(description="Port scanner")
	parser.add_argument("-t", "--target", required=True, dest="target", help="Target ip")
	parser.add_argument("-p", "--ports", required=True, dest="ports", help="Ports")
	options = parser.parse_args()

	return options.target, options.ports

def parse_ports(ports_str):
	if '-' in ports_str:
		start, end = map(int, ports_str.split('-'))
		return range(start, end+1)
	if ',' in ports_str:
		return map(int, ports_str.split(','))
	return [int(ports_str)]

def scan_port(host, port):
	socket = create_socket()
	try:
		socket.connect((host, port))
		socket.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
		response = socket.recv(1024)
		response = response.decode(errors='ignore').split("\n")[0]
		if response:
			print(colored(f"OK -> {response}", "green"))
		else:
			print(colored("OK", "green"))
	except (socket.timeout, ConnectionRefusedError):
		pass
	finally:
		socket.close()

def create_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	open_sockets.append(s)
	return s

if __name__ == "__main__":
	main()
